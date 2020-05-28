from enum import Enum, auto


class GameState(Enum):
    NOT_STARTED = auto()
    SETUP = auto()
    SETUP_REV = auto()
    SETUP_SETTLE_SEL = auto()
    SETUP_ROAD_SEL = auto()
    SETUP_REV_SETTLE_SEL = auto()
    SETUP_REV_ROAD_SEL = auto()
    PRE_ROLL = auto()
    ROBBER_SEL = auto()
    KNIGHT_SEL = auto()
    PLAYER_ROB_SEL = auto()
    NORMAL = auto()
    ROAD_SEL = auto()
    SETTLE_SEL = auto()
    CITY_SEL = auto()

    def get_trans_map(self):
        transition_map = {
            GameState.NOT_STARTED: {Transitions.START_GAME: GameState.SETUP},
            GameState.SETUP: {Transitions.END_TURN: GameState.SETUP,  # TODO end turn transition
                              Transitions.START_SETTLE_SEL: GameState.SETUP_SETTLE_SEL,
                              Transitions.START_ROAD_SEL: GameState.SETUP_ROAD_SEL},
            GameState.SETUP_REV: {Transitions.END_TURN: GameState.SETUP_REV,  # TODO end turn transition
                                  Transitions.START_SETTLE_SEL: GameState.SETUP_REV_SETTLE_SEL,
                                  Transitions.START_ROAD_SEL: GameState.SETUP_REV_ROAD_SEL},
            GameState.SETUP_SETTLE_SEL: {Transitions.CHOSE_SETTLE: GameState.SETUP},
            GameState.SETUP_ROAD_SEL: {Transitions.CHOSE_ROAD: GameState.SETUP},
            GameState.SETUP_REV_SETTLE_SEL: {Transitions.CHOSE_SETTLE: GameState.SETUP_REV},
            GameState.SETUP_REV_ROAD_SEL: {Transitions.CHOSE_ROAD: GameState.SETUP_REV},
            GameState.PRE_ROLL: {Transitions.ROLL_DICE: GameState.NORMAL, Transitions.ROLL_SEVEN: GameState.ROBBER_SEL},
            GameState.ROBBER_SEL: {Transitions.CHOSE_ROBBER: GameState.PLAYER_ROB_SEL},
            GameState.KNIGHT_SEL: {Transitions.CHOSE_ROBBER: GameState.PLAYER_ROB_SEL},
            GameState.PLAYER_ROB_SEL: {Transitions.CHOSE_PLAYER_ROB: GameState.NORMAL},
            GameState.NORMAL: {Transitions.START_ROAD_SEL: GameState.ROAD_SEL,
                               Transitions.START_SETTLE_SEL: GameState.SETTLE_SEL,
                               Transitions.START_CITY_SEL: GameState.CITY_SEL,
                               Transitions.USE_KNIGHT: GameState.KNIGHT_SEL},
            GameState.ROAD_SEL: {Transitions.CHOSE_ROAD: GameState.NORMAL},
            GameState.SETTLE_SEL: {Transitions.CHOSE_SETTLE: GameState.NORMAL},
            GameState.CITY_SEL: {Transitions.CHOSE_CITY: GameState.NORMAL}
        }
        return transition_map[self]

    def is_setup(self):
        return self in [self.SETUP, self.SETUP_REV, self.SETUP_ROAD_SEL,
                        self.SETUP_REV_ROAD_SEL, self.SETUP_SETTLE_SEL, self.SETUP_REV_SETTLE_SEL]

    def is_valid_transition(self, transition):
        return transition in self.get_trans_map()

    def get_next_state(self, transition):
        next_state = self.get_trans_map()[transition]
        return next_state


class Transitions(Enum):
    START_GAME = auto()
    CHOSE_ROAD = auto()
    CHOSE_SETTLE = auto()
    CHOSE_CITY = auto()
    CHOSE_ROBBER = auto()
    CHOSE_PLAYER_ROB = auto()
    START_ROAD_SEL = auto()
    START_SETTLE_SEL = auto()
    START_CITY_SEL = auto()
    START_ROBBER_SEL = auto()
    END_TURN = auto()
    ROLL_DICE = auto()
    ROLL_SEVEN = auto()
    USE_KNIGHT = auto()
