import server_controller.catan_server as cs
import json


class ServerPlayer:
    def __init__(self, plyr_id, socket, name, color):
        self.plyr_id = plyr_id
        self.web_socket = socket
        self.name = name
        self.color = color
        self.is_ready = False

    def get_summary_data(self):
        return {cs.NAME: self.name, cs.COLOR: self.color, cs.IS_READY: self.is_ready}

    async def send_created_room(self, room_id):
        print("{}: Sent created room".format(self.plyr_id))
        return_msg = {cs.TYPE: cs.CREATED_ROOM, cs.ROOM_ID: room_id, cs.PLAYER_ID: str(self.plyr_id), cs.COLOR: self.color}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_player_joined(self, plyr_name, plyr_color):
        print("{}: Sent player joined".format(self.plyr_id))
        return_msg = {cs.TYPE: cs.PLAYER_JOINED, cs.NAME: plyr_name, cs.COLOR: plyr_color}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_joined_room(self, other_plyrs_data):
        print("{}: Sent joined room".format(self.plyr_id))
        return_msg = {cs.TYPE: cs.JOINED_ROOM,
                      cs.PLAYER_ID: str(self.plyr_id),
                      cs.COLOR: self.color,
                      cs.OTHER_PLAYERS: other_plyrs_data}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_ready_success(self):
        self.is_ready = True
        return_msg = {cs.TYPE: cs.READY_SUCCESS}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_player_ready(self, plyr_name):
        return_msg = {cs.TYPE: cs.PLAYER_READY, cs.NAME: plyr_name}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_error(self, msg):
        return_msg = {cs.TYPE: cs.ERROR, cs.MSG: msg}
        await self.web_socket.send(json.dumps(return_msg))

    async def send_game_start(self, ports_html, tiles_html, numbers_html):
        return_msg = {cs.TYPE: cs.GAME_START,
                      cs.PORTS_HTML: ports_html, 
                      cs.TILES_HTML: tiles_html,
                      cs.NUMBERS_HTML: numbers_html}
        await self.web_socket.send(json.dumps(return_msg))
