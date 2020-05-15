from server_controller.waiting_room import Room
import server_controller.input_messages as im
import random
import json


# Incoming types
CREATE_ROOM = "CREATE_ROOM"
JOIN_ROOM = "JOIN_ROOM"
READY = "READY"
START_GAME = "START_GAME"
START_SETTLE_SELECT = "START_SETTLE_SELECT"
START_ROAD_SELECT = "START_ROAD_SELECT"
CHOSE_SETTLE = "CHOSE_SETTLE"
CHOSE_ROAD = "CHOSE_ROAD"
END_TURN = "END_TURN"

# Outgoing types
CREATED_ROOM = "CREATED_ROOM"
JOINED_ROOM = "JOINED_ROOM"
PLAYER_JOINED = "PLAYER_JOINED"
READY_SUCCESS = "READY_SUCCESS"
PLAYER_READY = "PLAYER_READY"
ERROR = "ERROR"
GAME_START = "GAME_START"
AVAIL_SETTLES = "AVAIL_SETTLES"
AVAIL_ROADS = "AVAIL_ROADS"
SETTLE_BUILT = "SETTLE_BUILT"
ROAD_BUILT = "ROAD_BUILT"
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
AVAIL = "avail"


class CatanServer:
    def __init__(self):
        self.games = {}
        self.client_ids = set()
        self.rooms = {}

    async def consumer_handler(self, websocket, path):
        async for message in websocket:
            await self.consumer(websocket, json.loads(message))

    async def consumer(self, websocket, msg):
        constructor_map = {
            CREATE_ROOM: lambda m, ws: im.CreateRoomMsg(m, ws, self.create_room),
            JOIN_ROOM: im.JoinRoomMsg,
            READY: im.ReadyMsg,
            START_GAME: im.StartGameMsg,
            START_SETTLE_SELECT: im.StartSettleSelectMsg,
            START_ROAD_SELECT: im.StartRoadSelectMsg,
            CHOSE_SETTLE: im.SettleBuiltMsg,
            CHOSE_ROAD: im.RoadBuiltMsg,
            END_TURN: im.EndTurnMsg
        }
        if TYPE not in msg or msg[TYPE] not in constructor_map:
            print("Malformed message: {}".format(msg))
            return

        msg_object = constructor_map[msg[TYPE]](msg, websocket)
        await msg_object.handle_message(self.rooms)

    def generate_room_id(self):
        room_id = random.randint(100000, 999999)
        while room_id in self.rooms:
            room_id = random.randint(100000, 999999)
        return room_id

    def create_room(self):
        room_id = self.generate_room_id()
        room = Room(room_id)
        self.rooms[room.room_id] = room
        return room
