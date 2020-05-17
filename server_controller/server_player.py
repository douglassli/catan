import server_controller.message_values as mv
import json


class ServerPlayer:
    def __init__(self, plyr_id, socket, name, color):
        self.plyr_id = plyr_id
        self.web_socket = socket
        self.name = name
        self.color = color
        self.is_ready = False

    def get_summary_data(self):
        return {mv.NAME: self.name,
                mv.COLOR: self.color,
                mv.IS_READY: self.is_ready}

    async def send_msg(self, msg):
        print("OUT: {}".format(msg))
        await self.web_socket.send(json.dumps(msg))

    async def send_created_room(self, room_id):
        return_msg = {mv.TYPE: mv.CREATED_ROOM,
                      mv.ROOM_ID: room_id,
                      mv.PLAYER_ID: self.plyr_id,
                      mv.COLOR: self.color}
        await self.send_msg(return_msg)

    async def send_player_joined(self, plyr_name, plyr_color):
        return_msg = {mv.TYPE: mv.PLAYER_JOINED,
                      mv.NAME: plyr_name,
                      mv.COLOR: plyr_color}
        await self.send_msg(return_msg)

    async def send_joined_room(self, other_plyrs_data):
        return_msg = {mv.TYPE: mv.JOINED_ROOM,
                      mv.PLAYER_ID: self.plyr_id,
                      mv.COLOR: self.color,
                      mv.OTHER_PLAYERS: other_plyrs_data}
        await self.send_msg(return_msg)

    async def send_ready_success(self):
        self.is_ready = True
        return_msg = {mv.TYPE: mv.READY_SUCCESS}
        await self.send_msg(return_msg)

    async def send_player_ready(self, plyr_name):
        return_msg = {mv.TYPE: mv.PLAYER_READY,
                      mv.NAME: plyr_name}
        await self.send_msg(return_msg)

    async def send_error(self, msg):
        return_msg = {mv.TYPE: mv.ERROR,
                      mv.MSG: msg}
        await self.send_msg(return_msg)

    async def send_game_start(self, ports_html, tiles_html, numbers_html, players_html, starting_name):
        return_msg = {mv.TYPE: mv.GAME_START,
                      mv.PORTS_HTML: ports_html,
                      mv.TILES_HTML: tiles_html,
                      mv.NUMBERS_HTML: numbers_html,
                      mv.PLAYERS_HTML: players_html,
                      mv.STARTING_PLAYER: starting_name}
        await self.send_msg(return_msg)

    async def display_options(self, msg_type, avail):
        return_msg = {mv.TYPE: msg_type,
                      mv.AVAIL: avail}
        await self.send_msg(return_msg)

    async def send_built(self, msg_type, row, col, color):
        return_msg = {mv.TYPE: msg_type,
                      mv.ROW: row,
                      mv.COL: col,
                      mv.COLOR: color}
        await self.send_msg(return_msg)

    async def send_start_turn(self, cur_name):
        return_msg = {mv.TYPE: mv.TURN_START,
                      mv.NAME: cur_name}
        await self.send_msg(return_msg)

    async def send_dice_rolled(self, roll_num, updates):
        return_msg = {mv.TYPE: mv.DICE_ROLLED,
                      mv.ROLL_NUM: roll_num,
                      mv.STATUS_UPDATES: updates}
        await self.send_msg(return_msg)
