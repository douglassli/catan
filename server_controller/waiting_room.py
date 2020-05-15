import uuid
from model.game_generator import generate_catan_game
from server_controller.templating import fill_tiles
from server_controller.server_player import ServerPlayer
import server_controller.message_values as mv


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
        new_player = ServerPlayer(uuid.uuid4(), websocket, name, self.get_next_color())
        self.players[new_player.plyr_id] = new_player
        other_players = [plyr for plyr in self.players.values() if plyr.plyr_id != new_player.plyr_id]

        if len(self.players) == 1:
            await new_player.send_created_room(self.room_id)
        else:
            await new_player.send_joined_room([other_plyr.get_summary_data() for other_plyr in other_players])
            for other_plyr in other_players:
                await other_plyr.send_player_joined(new_player.name, new_player.color)

    def has_plyr_id(self, plyr_id):
        return uuid.UUID(plyr_id) in self.players

    async def mark_ready(self, player_id):
        plyr_uuid = uuid.UUID(player_id)
        player = self.players[plyr_uuid]
        await player.send_ready_success()

        others = [other_plyr for other_plyr in self.players.values() if other_plyr.plyr_id != plyr_uuid]
        for other_plyr in others:
            await other_plyr.send_player_ready(player.name)

    def is_room_ready(self):
        return len(self.players) == 4 and all([plyr.is_ready for plyr in self.players.values()])

    async def start_game(self):
        player_data = [{"pid": plyr.plyr_id, "name": plyr.name, "color": plyr.color} for plyr in self.players.values()]
        self.game_model = generate_catan_game(player_data)
        self.has_started = True
        ports_html, tiles_html, numbers_html, player_bar = fill_tiles(self.game_model)
        starting_name = player_data[0]["name"]
        for player in self.players.values():
            await player.send_game_start(ports_html, tiles_html, numbers_html, player_bar, starting_name)

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
        if cur_player.pid == uuid.UUID(plyr_id) and (can_build or self.is_setup) and len(avail) > 0:
            self.is_selecting = True
            await self.players[uuid.UUID(plyr_id)].display_options(msg_type, avail)

    async def settle_built(self, plyr_id, row, col):
        can_build = self.game_model.can_build_settle()
        await self.built(plyr_id, row, col, can_build, self.game_model.build_settle, mv.SETTLE_BUILT)

    async def road_built(self, plyr_id, row, col):
        can_build = self.game_model.can_build_road()
        await self.built(plyr_id, row, col, can_build, self.game_model.build_road, mv.ROAD_BUILT)

    async def built(self, plyr_id, row, col, can_build, builder, msg_type):
        cur_player = self.game_model.cur_player()
        if cur_player.pid == uuid.UUID(plyr_id) and self.is_selecting and (can_build or self.is_setup):
            self.is_selecting = False
            color = builder((row, col), self.is_setup)
            for player in self.players.values():
                await player.send_built(msg_type, row, col, color)

    async def end_turn(self):
        self.is_setup, self.is_reverse = self.game_model.change_turn(self.is_setup, self.is_reverse)
        cur_plyr = self.game_model.cur_player()
        for player in self.players.values():
            await player.send_start_turn(cur_plyr.name)
