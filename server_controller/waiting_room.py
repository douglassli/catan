import uuid
from model.game_generator import generate_catan_game
from server_controller.templating import fill_tiles, player_bar
from server_controller.server_player import ServerPlayer
import server_controller.message_values as mv
from model.resources import Resource


class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.players = {}
        self.remaining_colors = ["red", "blue", "green", "yellow"]
        self.game_model = None
        self.has_started = False

        self.is_setup = True
        self.is_reverse = False
        self.is_selecting = True

    def is_name_available(self, name):
        for player in self.players.values():
            if name == player.name:
                return False
        return True

    def get_next_color(self):
        return self.remaining_colors.pop()

    async def add_player(self, websocket, name):
        new_player = ServerPlayer(str(uuid.uuid4()), websocket, name, self.get_next_color())
        self.players[new_player.plyr_id] = new_player
        other_players = [plyr for plyr in self.players.values() if plyr.plyr_id != new_player.plyr_id]

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

        others = [other_plyr for other_plyr in self.players.values() if other_plyr.plyr_id != player_id]
        for other_plyr in others:
            await other_plyr.send_player_ready(player.name)

    def is_room_ready(self):
        return len(self.players) == 4 and all([plyr.is_ready for plyr in self.players.values()])

    async def start_game(self):
        player_data = [{"pid": plyr.plyr_id, "name": plyr.name, "color": plyr.color} for plyr in self.players.values()]
        self.game_model = generate_catan_game(player_data)
        self.has_started = True
        ports_html, tiles_html, numbers_html = fill_tiles(self.game_model)
        starting_name = player_data[0]["name"]
        for player in self.players.values():
            player_bar_html = player_bar(self.game_model, player.name)
            await player.send_game_start(ports_html, tiles_html, numbers_html, player_bar_html, starting_name)

        await self.start_settle_select(self.game_model.cur_player().pid)

    async def start_settle_select(self, plyr_id):
        can_build = self.game_model.can_build_settle()
        avail = self.game_model.get_available_settle_nodes(self.is_setup)
        await self.start_select(plyr_id, can_build, avail, mv.AVAIL_SETTLES)

    async def start_road_select(self, plyr_id):
        can_build = self.game_model.can_build_road()
        avail = self.game_model.get_avail_paths(self.is_setup)
        await self.start_select(plyr_id, can_build, avail, mv.AVAIL_ROADS)

    async def start_select(self, plyr_id, can_build, avail, msg_type):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and (can_build or self.is_setup) and len(avail) > 0:
            self.is_selecting = True
            await self.players[plyr_id].display_options(msg_type, avail)

    async def settle_built(self, plyr_id, row, col):
        can_build = self.game_model.can_build_settle()
        await self.built(plyr_id, row, col, can_build, self.game_model.build_settle, mv.SETTLE_BUILT)

        if self.is_setup:
            await self.start_road_select(plyr_id)

    async def road_built(self, plyr_id, row, col):
        can_build = self.game_model.can_build_road()
        await self.built(plyr_id, row, col, can_build, self.game_model.build_road, mv.ROAD_BUILT)

        if self.is_setup:
            await self.end_turn(plyr_id)

        if self.is_setup:
            cur_plyr = self.game_model.cur_player()
            await self.start_settle_select(cur_plyr.pid)

    async def built(self, plyr_id, row, col, can_build, builder, msg_type):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == plyr_id and self.is_selecting and (can_build or self.is_setup):
            self.is_selecting = False
            color = builder((row, col), self.is_setup)
            for player in self.players.values():
                await player.send_built(msg_type, row, col, color)

    async def end_turn(self, plyr_id):
        cur_plyr = self.game_model.cur_player()
        if plyr_id == cur_plyr.pid and not self.is_selecting:
            self.is_setup, self.is_reverse = self.game_model.change_turn(self.is_setup, self.is_reverse)
            new_cur_plyr = self.game_model.cur_player()
            for player in self.players.values():
                await player.send_start_turn(new_cur_plyr.name)

    async def roll_dice(self, plyr_id):
        cur_plyr = self.game_model.cur_player()
        if plyr_id == cur_plyr.pid and not self.is_selecting and not self.is_setup:
            roll_num = self.game_model.roll_dice()
            if roll_num == 7:
                # TODO move robber
                pass
            else:
                self.game_model.distribute_resources(roll_num)
                for plyr in self.game_model.players:
                    updates = [{mv.NAME: p.name, mv.HAND_SIZE: p.get_hand_size()} for p in self.game_model.players if p.pid != plyr.pid]
                    updates.append({mv.NAME: plyr.name,
                                    mv.HAND_SIZE: plyr.get_hand_size(),
                                    mv.WOOD: plyr.resources[Resource.WOOD],
                                    mv.BRICK: plyr.resources[Resource.BRICK],
                                    mv.SHEEP: plyr.resources[Resource.SHEEP],
                                    mv.WHEAT: plyr.resources[Resource.WHEAT],
                                    mv.STONE: plyr.resources[Resource.STONE]})
                    await self.players[plyr.pid].send_dice_rolled(roll_num, updates)
