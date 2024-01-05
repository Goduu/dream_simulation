from enum import Enum


class ActionType(Enum):
    """
    Enum representing the types of actions a player can take.

    Values:
    MOVE: Represents a move action.
    PLAY_CARD: Represents a play card action.
    BUY_CARD: Represents a buy card action.
    """

    START = "start"
    MOVE = "move"
    MOVE_OUT = "move_out"
    DROP_ICE = "drop_ice"
    BUY_CARD = "buy_card"
    PLAY_CARD = "play_card"
    BREAK_ICE = "break_ice"
    FISHING = "fishing"
    TURN = "turn"


class Action:
    """
    Represents an action that a player can take during the game.

    Attributes:
    player (Player): The player who is taking the action.
    type (ActionType): The type of the action.
    target (Hexagon): The target of the action.
    """

    def __init__(self, action_type: ActionType, action_parameter):
        self.type = action_type
        self.parameter = action_parameter

    def __repr__(self):
        return f"\nAction: {self.type}, Parameter: {self.parameter}"
