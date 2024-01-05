from enum import Enum


class FishType(Enum):
    A = "A"
    B = "B"
    C = "C"


class Fish:
    """
    Represents a fish in the game.
    """

    def __init__(self, fish_type: FishType):
        self.type: FishType = fish_type

    def __repr__(self) -> str:
        return f"Fish {self.type.value}"
    
    def __eq__(self, other):
        return self.type == other.type


class Ice:
    """
    Represents an ice in the game.
    """

    def __init__(self):
        self.type = "ice"
        pass

    def __repr__(self) -> str:
        return f"Ice"
    
    def __eq__(self, other):
        return self.type == other.type


class BackpackItem:
    Ice or Fish
