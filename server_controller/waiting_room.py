import uuid


class Room:
    def __init__(self, room_id, init_player):
        self.room_id = room_id
        self.players = {init_player.plyr_id: init_player}
        self.remaining_colors = ["blue", "green", "yellow"]

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
