import json
from uuid import uuid4
from server_controller.server_player import ServerPlayer
from server_controller.waiting_room import Room
import random


# Incoming types
CREATE_ROOM = "CREATE_ROOM"
JOIN_ROOM = "JOIN_ROOM"
READY = "READY"
START_GAME = "START_GAME"
CHOSE_SETTLE = "CHOSE_SETTLE"
END_TURN = "END_TURN"

# Outgoing types
CREATED_ROOM = "CREATED_ROOM"
JOINED_ROOM = "JOINED_ROOM"
PLAYER_JOINED = "PLAYER_JOINED"
READY_SUCCESS = "READY_SUCCESS"
PLAYER_READY = "PLAYER_READY"
ERROR = "ERROR"
GAME_START = "GAME_START"
SETTLE_BUILT = "SETTLE_BUILT"
TURN_START = "TURN_START"

# Field names
TYPE = "type"
ROOM_ID = "roomID"
PLAYER_ID = "playerID"
NAME = "name"
COLOR = "color"
OTHER_PLAYERS = "otherPlayers"
MSG = "msg"
IS_READY = "isReady"
PORTS_HTML = "portsHTML"
TILES_HTML = "tilesHTML"
NUMBERS_HTML = "numbersHTML"
PLAYERS_HTML = "playersHTML"
ROW = "row"
COL = "col"
STARTING_PLAYER = "startingPlayer"


class CatanServer:
    def __init__(self):
        self.games = {}
        self.client_ids = set()
        self.rooms = {}

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consumer(websocket, json.loads(message))

    def log(self, msg):
        print(msg)

    async def consumer(self, websocket, msg):
        if TYPE in msg:
            msg_type = msg[TYPE]
        else:
            self.log("Malformed message: {}".format(msg))
            return

        if msg_type == CREATE_ROOM:
            await self.handle_create_room(msg, websocket)
        elif msg_type == JOIN_ROOM:
            await self.handle_join_room(msg, websocket)
        elif msg_type == READY:
            await self.handle_ready(msg)
        elif msg_type == START_GAME:
            await self.handle_start_game(msg, websocket)
        elif msg_type == CHOSE_SETTLE:
            await self.handle_settle_built(msg, websocket)
        elif msg_type == END_TURN:
            await self.handle_end_turn(msg, websocket)
        else:
            self.log("Unknown type: {}".format(msg))

    async def handle_create_room(self, msg, websocket):
        if not self.is_valid_create_room(msg):
            self.log("Invalid create room message: {}".format(msg))
        else:
            player = ServerPlayer(uuid4(), websocket, msg[NAME], "red")
            room = self.create_room(player)
            self.rooms[room.room_id] = room
            await player.send_created_room(room.room_id)

    async def handle_join_room(self, msg, websocket):
        if not self.is_valid_join_room(msg):
            self.log("Invalid join room message: {}".format(msg))
        else:
            room = self.rooms[msg[ROOM_ID]]
            player = ServerPlayer(uuid4(), websocket, msg[NAME], room.get_next_color())
            await room.add_player(player)

    async def handle_ready(self, msg):
        if not self.is_valid_ready(msg):
            self.log("Invalid ready message: {}".format(msg))
        else:
            room = self.rooms[msg[ROOM_ID]]
            await room.mark_ready(msg[PLAYER_ID])

    async def handle_start_game(self, msg, websocket):
        if not self.is_valid_start_game(msg):
            self.log("Invalid start game message: {}".format(msg))
        else:
            room = self.rooms[msg[ROOM_ID]]
            await room.start_game()

    async def handle_settle_built(self, msg, websocket):
        if not self.is_valid_settle_built(msg):
            self.log("Invalid settle built message: {}".format(msg))
        else:
            room = self.rooms[msg[ROOM_ID]]
            await room.settle_built(msg[PLAYER_ID], msg[ROW], msg[COL])

    async def handle_end_turn(self, msg, websocket):
        if not self.is_valid_end_turn(msg):
            self.log("Invalid end turn message: {}".format(msg))
        else:
            room = self.rooms[msg[ROOM_ID]]
            await room.end_turn(msg[PLAYER_ID])

    def check_ids(self, msg):
        room_id = msg[ROOM_ID]
        plyr_id = msg[PLAYER_ID]
        return room_id in self.rooms and self.rooms[room_id].has_plyr_id(plyr_id)

    def is_valid_create_room(self, msg):
        return msg[NAME].isalnum()

    def is_valid_join_room(self, msg):
        room_id = msg[ROOM_ID]
        name = msg[NAME]
        return room_id in self.rooms and name.isalnum() and self.rooms[room_id].is_name_available(name)

    def is_valid_ready(self, msg):
        return self.check_ids(msg)

    def is_valid_start_game(self, msg):
        return self.check_ids(msg) and self.rooms[msg[ROOM_ID]].is_room_ready()

    def is_valid_settle_built(self, msg):
        return self.check_ids(msg)

    def is_valid_end_turn(self, msg):
        return self.check_ids(msg)

    def generate_room_id(self):
        room_id = random.randint(100000, 999999)
        while room_id in self.rooms:
            room_id = random.randint(100000, 999999)
        return room_id

    def create_room(self, init_player):
        room_id = self.generate_room_id()
        room = Room(room_id, init_player)
        return room
