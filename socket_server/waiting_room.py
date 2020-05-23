import uuid
from model.game_generator import generate_catan_game
from http_server.templating import fill_tiles, player_bar
from socket_server.server_player import ServerPlayer
from socket_server.game_state import GameState, Transitions
import socket_server.message_values as mv
from model.resources import Resource


class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}
        self.remaining_colors = ["red", "blue", "green", "yellow"]
        self.game_model = None
        self.game_state = GameState.NOT_STARTED

    def is_name_available(self, name):
        for player in self.players.values():
            if name == player.name:
                return False
        return True

    def get_next_color(self):
        return self.remaining_colors.pop()

    async def add_player(self, websocket, name):
        new_player = ServerPlayer(str(uuid.uuid4()), websocket, name, self.get_next_color())
        self.players[new_player.pid] = new_player
        other_players = [plyr for plyr in self.players.values() if plyr.pid != new_player.pid]

        if len(self.players) == 1:
            await new_player.send_created_room(self.room_id)
        else:
            await new_player.send_joined_room([other_plyr.get_summary_data() for other_plyr in other_players])
            for other_plyr in other_players:
                await other_plyr.send_player_joined(new_player.name, new_player.color)

    def has_plyr_id(self, plyr_id):
        return plyr_id in self.players

    async def mark_ready(self, player_id):
        player = self.players[player_id]
        await player.send_ready_success()

        others = [other_plyr for other_plyr in self.players.values() if other_plyr.pid != player_id]
        for other_plyr in others:
            await other_plyr.send_player_ready(player.name)

    def is_room_ready(self):
        return len(self.players) == 4 and all([plyr.is_ready for plyr in self.players.values()])

    async def start_game(self):
        player_data = [{"pid": plyr.pid, "name": plyr.name, "color": plyr.color} for plyr in self.players.values()]
        self.game_model = generate_catan_game(player_data)
        self.game_state = self.game_state.get_next_state(Transitions.START_GAME)
        ports_html, tiles_html, numbers_html = fill_tiles(self.game_model)
        starting_name = player_data[0]["name"]
        for player in self.players.values():
            player_bar_html = player_bar(self.game_model, player.name)
            await player.send_game_start(ports_html, tiles_html, numbers_html, player_bar_html, starting_name)

        await self.start_settle_select(self.game_model.cur_player().pid)

    async def start_settle_select(self, plyr_id):
        can_build = self.game_model.can_build_settle() or self.game_state.is_setup()
        avail = self.game_model.get_available_settle_nodes(self.game_state.is_setup())
        await self.start_select(plyr_id, can_build, avail, mv.AVAIL_SETTLES, Transitions.START_SETTLE_SEL)

    async def start_road_select(self, plyr_id):
        can_build = self.game_model.can_build_road() or self.game_state.is_setup()
        avail = self.game_model.get_avail_paths(self.game_state.is_setup())
        await self.start_select(plyr_id, can_build, avail, mv.AVAIL_ROADS, Transitions.START_ROAD_SEL)

    async def start_city_select(self, plyr_id):
        can_build = self.game_model.can_build_city()
        avail = self.game_model.get_avail_cities(self.game_state.is_setup())
        await self.start_select(plyr_id, can_build, avail, mv.AVAIL_CITIES, Transitions.START_CITY_SEL)

    async def start_select(self, plyr_id, can_build, avail, msg_type, transition):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and self.game_state.is_valid_transition(transition) and can_build and len(avail) > 0:
            self.game_state = self.game_state.get_next_state(transition)
            await self.players[plyr_id].display_options(msg_type, avail)

    async def chose_settle(self, plyr_id, row, col):
        can_build = self.game_model.can_build_settle() or self.game_state.is_setup()
        await self.chose(plyr_id, row, col, can_build, self.game_model.build_settle,
                         mv.SETTLE_BUILT, Transitions.CHOSE_SETTLE)

        # TODO Check if chose was successful, if not, don't do next steps
        if self.game_state == GameState.SETUP or self.game_state == GameState.SETUP_REV:
            await self.start_road_select(plyr_id)

    async def chose_road(self, plyr_id, row, col):
        can_build = self.game_model.can_build_road() or self.game_state.is_setup()
        await self.chose(plyr_id, row, col, can_build, self.game_model.build_road,
                         mv.ROAD_BUILT, Transitions.CHOSE_ROAD)

        if self.game_state == GameState.SETUP or self.game_state == GameState.SETUP_REV:
            await self.end_turn(plyr_id)

        if self.game_state == GameState.SETUP or self.game_state == GameState.SETUP_REV:
            cur_plyr = self.game_model.cur_player()
            await self.start_settle_select(cur_plyr.pid)

    async def chose_city(self, plyr_id, row, col):
        can_build = self.game_model.can_build_city()
        await self.chose(plyr_id, row, col, can_build, self.game_model.build_city,
                         mv.CITY_BUILT, Transitions.CHOSE_CITY)

    async def chose(self, plyr_id, row, col, can_build, builder, msg_type, transition):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and self.game_state.is_valid_transition(transition) and can_build:
            self.game_state = self.game_state.get_next_state(transition)
            color = builder((row, col), self.game_state.is_setup())

            if self.game_state == GameState.SETUP_REV and transition == Transitions.CHOSE_SETTLE:
                self.game_model.give_setup_resources((row, col))

            deck_state = self.get_deck_state()
            for plyr in self.players.values():
                active_buttons = self.get_active_buttons() if cur_player.pid == plyr.pid else None
                updates = self.get_updates(plyr)
                await plyr.send_built(msg_type, row, col, color, updates, deck_state, active_buttons)

    async def end_turn(self, plyr_id):
        cur_plyr = self.game_model.cur_player()
        if plyr_id == cur_plyr.pid and self.game_state in [GameState.NORMAL, GameState.SETUP, GameState.SETUP_REV]:
            self.game_state = self.game_model.change_turn(self.game_state)
            new_cur_plyr = self.game_model.cur_player()
            for player in self.players.values():
                active_buttons = self.get_active_buttons() if new_cur_plyr.pid == player.pid else None
                await player.send_start_turn(new_cur_plyr.name, active_buttons)

    async def roll_dice(self, plyr_id):
        cur_plyr = self.game_model.cur_player()
        if plyr_id == cur_plyr.pid and self.game_state.is_valid_transition(Transitions.ROLL_DICE):
            roll_num1, roll_num2 = self.game_model.roll_dice()
            if roll_num1 + roll_num2 == 7:
                self.game_state = self.game_state.get_next_state(Transitions.ROLL_SEVEN)
                avail = self.game_model.get_avail_robber_coords()
                await self.players[cur_plyr.pid].display_options(mv.AVAIL_ROBBERS, avail)
                for plyr in self.players.values():
                    await plyr.send_dice_rolled(roll_num1, roll_num2, [], {}, None)
            else:
                self.game_state = self.game_state.get_next_state(Transitions.ROLL_DICE)
                self.game_model.distribute_resources(roll_num1 + roll_num2)
                deck_state = self.get_deck_state()
                for plyr in self.players.values():
                    updates = self.get_updates(plyr)
                    active_buttons = self.get_active_buttons() if cur_plyr.pid == plyr.pid else None
                    await plyr.send_dice_rolled(roll_num1, roll_num2, updates, deck_state, active_buttons)

    async def robber_moved(self, plyr_id, row, col):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and self.game_state.is_valid_transition(Transitions.CHOSE_ROBBER):
            self.game_state = self.game_state.get_next_state(Transitions.CHOSE_ROBBER)
            prev_coord = self.game_model.get_robber_coord()
            self.game_model.move_robber((row, col))
            avail = self.game_model.get_avail_to_rob((row, col))
            if len(avail) == 0:
                self.game_state = self.game_state.get_next_state(Transitions.CHOSE_PLAYER_ROB)
            for player in self.players.values():
                active_buttons = self.get_active_buttons() if cur_player.pid == player.pid else None
                avail_to_rob = avail if player.pid == cur_player.pid and len(avail) > 0 else None
                await player.send_robber_moved(row, col, prev_coord[0], prev_coord[1], active_buttons, avail_to_rob)

    async def chose_player_rob(self, plyr_id, robbed_name):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and self.game_model.can_rob(robbed_name) and self.game_state.is_valid_transition(Transitions.CHOSE_PLAYER_ROB):
            self.game_state = self.game_state.get_next_state(Transitions.CHOSE_PLAYER_ROB)
            self.game_model.rob_player(robbed_name)
            robbed_player = self.game_model.get_player_by_name(robbed_name)
            cur_update = {mv.NAME: cur_player.name, mv.HAND_SIZE: cur_player.get_hand_size()}
            robbed_update = {mv.NAME: robbed_player.name, mv.HAND_SIZE: robbed_player.get_hand_size()}
            for player in self.players.values():
                active_buttons = self.get_active_buttons() if cur_player.pid == player.pid else None
                if player.pid == cur_player.pid:
                    updates = [self.get_private_state(cur_player), robbed_update]
                elif player.pid == robbed_player.pid:
                    updates = [self.get_private_state(robbed_player), cur_update]
                else:
                    updates = [robbed_update, cur_update]
                await player.send_player_robbed(cur_player.name, robbed_name, updates, active_buttons)

    async def buy_dev_card(self, plyr_id):
        cur_plyr = self.game_model.cur_player()
        if cur_plyr.pid == plyr_id and self.game_state == GameState.NORMAL and cur_plyr.can_buy_dev_card():
            self.game_model.buy_dev_card()
            deck_state = self.get_deck_state()
            updates = self.get_updates(cur_plyr)
            for plyr in self.players.values():
                active_buttons = self.get_active_buttons() if cur_plyr.pid == plyr.pid else None
                await plyr.send_bought_dev_card(cur_plyr.name, updates, deck_state, active_buttons)

    def get_deck_state(self):
        return {
            mv.WOOD: self.game_model.resources[Resource.WOOD],
            mv.BRICK: self.game_model.resources[Resource.BRICK],
            mv.SHEEP: self.game_model.resources[Resource.SHEEP],
            mv.WHEAT: self.game_model.resources[Resource.WHEAT],
            mv.STONE: self.game_model.resources[Resource.STONE],
            mv.DEV_CARDS: len(self.game_model.dev_cards)
        }

    def get_public_state(self, player):
        return {
            mv.NAME: player.name,
            mv.VPS: player.get_victory_points(),
            mv.ROADS: player.num_roads,
            mv.SETTLES: player.num_settles,
            mv.CITIES: player.num_cities,
            mv.HAND_SIZE: player.get_hand_size(),
            mv.DEV_CARDS: player.get_dev_card_hand_size(),
            mv.ROAD_LENGTH: player.road_length,
            mv.ARMY_SIZE: player.army_size
        }

    def get_private_state(self, player):
        public = self.get_public_state(player)
        public[mv.WOOD] = player.resources[Resource.WOOD]
        public[mv.BRICK] = player.resources[Resource.BRICK]
        public[mv.SHEEP] = player.resources[Resource.SHEEP]
        public[mv.WHEAT] = player.resources[Resource.WHEAT]
        public[mv.STONE] = player.resources[Resource.STONE]
        return public

    def get_updates(self, cur_plyr):
        updates = []
        for plyr in self.game_model.players:
            if plyr.pid == cur_plyr.pid:
                updates.append(self.get_private_state(plyr))
            else:
                updates.append(self.get_public_state(plyr))
        return updates

    def get_active_buttons(self):
        buttons = []
        cur_plyr = self.game_model.cur_player()
        is_normal = self.game_state == GameState.NORMAL
        if self.game_state == GameState.PRE_ROLL:
            buttons.append(mv.ROLL_BUTTON)
        if is_normal:
            buttons.append(mv.END_TURN_BUTTON)
        if cur_plyr.can_buy_dev_card() and is_normal:
            buttons.append(mv.DEV_BUTTON)
        if cur_plyr.can_build_city() and is_normal:
            buttons.append(mv.CITY_BUTTON)
        if cur_plyr.can_build_settle() and is_normal:
            buttons.append(mv.SETTLE_BUTTON)
        if cur_plyr.can_build_road() and is_normal:
            buttons.append(mv.ROAD_BUTTON)
        if is_normal:
            buttons.append(mv.TRADE_BUTTON)
        return buttons