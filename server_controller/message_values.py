import server_controller.input_messages as im
from enum import Enum


class InTypes(Enum):
    CREATE_ROOM = "CREATE_ROOM"
    JOIN_ROOM = "JOIN_ROOM"
    READY = "READY"
    START_GAME = "START_GAME"
    START_SETTLE_SELECT = "START_SETTLE_SELECT"
    START_ROAD_SELECT = "START_ROAD_SELECT"
    CHOSE_SETTLE = "CHOSE_SETTLE"
    CHOSE_ROAD = "CHOSE_ROAD"
    END_TURN = "END_TURN"

    @classmethod
    def is_member(cls, value):
        return any([value == item.value for item in cls])

    def create_msg_object(self, msg, websocket):
        constructor_map = {
            self.CREATE_ROOM: im.CreateRoomMsg,
            self.JOIN_ROOM: im.JoinRoomMsg,
            self.READY: im.ReadyMsg,
            self.START_GAME: im.StartGameMsg,
            self.START_SETTLE_SELECT: im.StartSettleSelectMsg,
            self.START_ROAD_SELECT: im.StartRoadSelectMsg,
            self.CHOSE_SETTLE: im.SettleBuiltMsg,
            self.CHOSE_ROAD: im.RoadBuiltMsg,
            self.END_TURN: im.EndTurnMsg
        }
        return constructor_map[self](msg, websocket)


class OutTypes(Enum):
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


class FieldNames(Enum):
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
