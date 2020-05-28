import socket_server.message_values as mv
import json


class ServerPlayer:
    def __init__(self, plyr_id, socket, name, color):
        self.pid = plyr_id
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
                      mv.PLAYER_ID: self.pid,
                      mv.COLOR: self.color}
        await self.send_msg(return_msg)

    async def send_player_joined(self, plyr_name, plyr_color):
        return_msg = {mv.TYPE: mv.PLAYER_JOINED,
                      mv.NAME: plyr_name,
                      mv.COLOR: plyr_color}
        await self.send_msg(return_msg)

    async def send_joined_room(self, other_plyrs_data):
        return_msg = {mv.TYPE: mv.JOINED_ROOM,
                      mv.PLAYER_ID: self.pid,
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

    async def send_built(self, msg_type, row, col, color, updates, deck_state, active_buttons):
        return_msg = {mv.TYPE: msg_type,
                      mv.ROW: row,
                      mv.COL: col,
                      mv.COLOR: color,
                      mv.STATUS_UPDATES: updates,
                      mv.DECK_UPDATE: deck_state}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)

    async def send_start_turn(self, cur_name, active_buttons):
        return_msg = {mv.TYPE: mv.TURN_START,
                      mv.NAME: cur_name}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)

    async def send_dice_rolled(self, roll_num1, roll_num2, updates, deck_state, active_buttons):
        return_msg = {mv.TYPE: mv.DICE_ROLLED,
                      mv.ROLL_NUM1: roll_num1,
                      mv.ROLL_NUM2: roll_num2,
                      mv.STATUS_UPDATES: updates,
                      mv.DECK_UPDATE: deck_state}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)

    async def send_robber_moved(self, row, col, prev_row, prev_col, active_buttons, avail_to_rob, status):
        return_msg = {mv.TYPE: mv.ROBBER_MOVED,
                      mv.ROW: row,
                      mv.COL: col,
                      mv.PREV_ROW: prev_row,
                      mv.PREV_COL: prev_col}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        if avail_to_rob is not None:
            return_msg[mv.AVAIL_TO_ROB] = avail_to_rob
        if status is not None:
            return_msg[mv.STATUS_UPDATES] = status
        await self.send_msg(return_msg)

    async def send_player_robbed(self, player_gained, player_robbed, updates, active_buttons):
        return_msg = {mv.TYPE: mv.ROBBER_MOVED,
                      mv.PLAYER_GAINED: player_gained,
                      mv.PLAYER_ROBBED: player_robbed,
                      mv.STATUS_UPDATES: updates}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)

    async def send_bought_dev_card(self, name, updates, deck_state, active_buttons):
        return_msg = {mv.TYPE: mv.BOUGHT_DEV_CARD,
                      mv.NAME: name,
                      mv.STATUS_UPDATES: updates,
                      mv.DECK_UPDATE: deck_state}
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)

    async def send_trade_proposed(self, proposer_name, trade_id, cur_resources, other_resources, can_accept):
        return_msg = {mv.TYPE: mv.TRADE_PROPOSED,
                      mv.NAME: proposer_name,
                      mv.TRADE_ID: trade_id,
                      mv.CURRENT_RESOURCES: {mv.res_to_field(res): num for res, num in cur_resources.items()},
                      mv.OTHER_RESOURCES: {mv.res_to_field(res): num for res, num in other_resources.items()},
                      mv.CAN_ACCEPT: can_accept}
        await self.send_msg(return_msg)

    async def send_trade_responded(self, responder_name, trade_id, accepted):
        return_msg = {mv.TYPE: mv.TRADE_RESPONDED,
                      mv.NAME: responder_name,
                      mv.TRADE_ID: trade_id,
                      mv.ACCEPTED: accepted}
        await self.send_msg(return_msg)

    async def send_trade_closed(self, trade_id, updates, deck_state, active_buttons=None):
        return_msg = {mv.TYPE: mv.TRADE_CLOSED,
                      mv.TRADE_ID: trade_id}
        if updates is not None:
            return_msg[mv.STATUS_UPDATES] = updates
        if deck_state is not None:
            return_msg[mv.DECK_UPDATE] = deck_state
        if active_buttons is not None:
            return_msg[mv.ACTIVE_BUTTONS] = active_buttons
        await self.send_msg(return_msg)
