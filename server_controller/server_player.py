from server_controller.message_values import FieldNames
import json


class ServerPlayer:
    def __init__(self, plyr_id, socket, name, color):
        self.plyr_id = plyr_id
        self.web_socket = socket
        self.name = name
        self.color = color
        self.is_ready = False

    def get_summary_data(self):
        return {FieldNames.NAME: self.name,
                FieldNames.COLOR: self.color,
                FieldNames.IS_READY: self.is_ready}

    async def send_created_room(self, room_id):
        print("{}: Sent created room".format(self.plyr_id))
        return_msg = {FieldNames.TYPE: FieldNames.CREATED_ROOM,
                      FieldNames.ROOM_ID: room_id,
                      FieldNames.PLAYER_ID: str(self.plyr_id),
                      FieldNames.COLOR: self.color}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_player_joined(self, plyr_name, plyr_color):
        print("{}: Sent player joined".format(self.plyr_id))
        return_msg = {FieldNames.TYPE: FieldNames.PLAYER_JOINED,
                      FieldNames.NAME: plyr_name,
                      FieldNames.COLOR: plyr_color}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_joined_room(self, other_plyrs_data):
        print("{}: Sent joined room".format(self.plyr_id))
        return_msg = {FieldNames.TYPE: FieldNames.JOINED_ROOM,
                      FieldNames.PLAYER_ID: str(self.plyr_id),
                      FieldNames.COLOR: self.color,
                      FieldNames.OTHER_PLAYERS: other_plyrs_data}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_ready_success(self):
        self.is_ready = True
        return_msg = {FieldNames.TYPE: FieldNames.READY_SUCCESS}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_player_ready(self, plyr_name):
        return_msg = {FieldNames.TYPE: FieldNames.PLAYER_READY,
                      FieldNames.NAME: plyr_name}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_error(self, msg):
        return_msg = {FieldNames.TYPE: FieldNames.ERROR,
                      FieldNames.MSG: msg}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_game_start(self, ports_html, tiles_html, numbers_html, players_html, starting_name):
        return_msg = {FieldNames.TYPE: FieldNames.GAME_START,
                      FieldNames.PORTS_HTML: ports_html,
                      FieldNames.TILES_HTML: tiles_html,
                      FieldNames.NUMBERS_HTML: numbers_html,
                      FieldNames.PLAYERS_HTML: players_html,
                      FieldNames.STARTING_PLAYER: starting_name}
        await self.web_socket.send(json.dumps(return_msg))

    async def display_options(self, msg_type, avail):
        return_msg = {FieldNames.TYPE: msg_type,
                      FieldNames.AVAIL: avail}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_built(self, msg_type, row, col, color):
        return_msg = {FieldNames.TYPE: msg_type,
                      FieldNames.ROW: row,
                      FieldNames.COL: col,
                      FieldNames.COLOR: color}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_start_turn(self, cur_name):
        return_msg = {FieldNames.TYPE: FieldNames.TURN_START,
                      FieldNames.NAME: cur_name}
        await self.web_socket.send(json.dumps(return_msg))
