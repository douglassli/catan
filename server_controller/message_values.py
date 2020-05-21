import server_controller.input_messages as im
from enum import Enum


class InTypes(Enum):
    CREATE_ROOM = "CREATE_ROOM"
    JOIN_ROOM = "JOIN_ROOM"
    READY = "READY"
    START_GAME = "START_GAME"
    START_SETTLE_SELECT = "START_SETTLE_SELECT"
    START_ROAD_SELECT = "START_ROAD_SELECT"
    START_CITY_SELECT = "START_CITY_SELECT"
    CHOSE_SETTLE = "CHOSE_SETTLE"
    CHOSE_ROAD = "CHOSE_ROAD"
    CHOSE_CITY = "CHOSE_CITY"
    END_TURN = "END_TURN"
    ROLL_DICE = "ROLL_DICE"
    CHOSE_ROBBER = "CHOSE_ROBBER"

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
            self.START_CITY_SELECT: im.StartCitySelectMsg,
            self.CHOSE_SETTLE: im.ChoseSettleMsg,
            self.CHOSE_ROAD: im.ChoseRoadMsg,
            self.CHOSE_CITY: im.ChoseCityMsg,
            self.END_TURN: im.EndTurnMsg,
            self.ROLL_DICE: im.RollDiceMsg,
            self.CHOSE_ROBBER: im.ChoseRobberMsg
        }
        return constructor_map[self](msg, websocket)


# Outgoing message types
CREATED_ROOM = "CREATED_ROOM"
JOINED_ROOM = "JOINED_ROOM"
PLAYER_JOINED = "PLAYER_JOINED"
READY_SUCCESS = "READY_SUCCESS"
PLAYER_READY = "PLAYER_READY"
ERROR = "ERROR"
GAME_START = "GAME_START"
AVAIL_SETTLES = "AVAIL_SETTLES"
AVAIL_ROADS = "AVAIL_ROADS"
AVAIL_CITIES = "AVAIL_CITIES"
SETTLE_BUILT = "SETTLE_BUILT"
ROAD_BUILT = "ROAD_BUILT"
CITY_BUILT = "CITY_BUILT"
TURN_START = "TURN_START"
DICE_ROLLED = "DICE_ROLLED"
AVAIL_ROBBERS = "AVAIL_ROBBERS"
ROBBER_MOVED = "ROBBER_MOVED"

# Message field names
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
PREV_ROW = "prevRow"
PREV_COL = "prevCol"
STARTING_PLAYER = "startingPlayer"
AVAIL = "avail"
ROLL_NUM = "rollNum"
STATUS_UPDATES = "statusUpdates"
DECK_UPDATE = "deckUpdate"
VPS = "vps"
ROADS = "roads"
HAND_SIZE = "handSize"
SETTLES = "settles"
DEV_CARDS = "devCards"
CITIES = "cities"
ROAD_LENGTH = "roadLength"
ARMY_SIZE = "armySize"
WOOD = "wood"
BRICK = "brick"
SHEEP = "sheep"
WHEAT = "wheat"
STONE = "stone"
ACTIVE_BUTTONS = "activeButtons"

# Button Ids
TRADE_BUTTON = "tradeButton"
ROAD_BUTTON = "buyRoadButton"
SETTLE_BUTTON = "buySettleButton"
CITY_BUTTON = "buyCityButton"
DEV_BUTTON = "buyDevCardButton"
ROLL_BUTTON = "rollButton"
END_TURN_BUTTON = "endTurnButton"
