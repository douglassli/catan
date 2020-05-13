import uuid
from model.game_generator import generate_catan_game
from server_controller.templating import fill_tiles


class Room:
    def __init__(self, room_id, init_player):
        self.room_id = room_id
        self.players = {init_player.plyr_id: init_player}
        self.remaining_colors = ["blue", "green", "yellow"]
        self.game_model = None
        self.has_started = False

    def is_name_available(self, name):
        for player in self.players.values():
            if name == player.name:
                return False
        return True

    def get_next_color(self):
        return self.remaining_colors.pop()

    async def add_player(self, new_player):
        self.players[new_player.plyr_id] = new_player
        other_players = [plyr for plyr in self.players.values() if plyr.plyr_id != new_player.plyr_id]
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
        self.game_model = generate_catan_game()
        self.has_started = True
        ports_html, tiles_html, numbers_html = fill_tiles(self.game_model.tiles.values())
        for player in self.players.values():
            await player.send_game_start(ports_html, tiles_html, numbers_html)
