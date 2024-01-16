from enum import Enum
import json


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

    def to_json(self):
        """
        Serializes the Fish object to a JSON-formatted string.
        """
        return json.dumps(
            {
                "type": self.type.value,
            }
        )

    @staticmethod
    def from_json(json_str):
        """
        Deserializes the JSON-formatted string to a Fish object.
        Note: This method assumes the JSON string is in the correct format.
        """
        data = json.loads(json_str)
        return Fish(fish_type=data.type)


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

    def to_json(self):
        """
        Serializes the Fish object to a JSON-formatted string.
        """
        return json.dumps(
            {
                "type": self.type,
            }
        )

    def from_json(json_str):
        """
        Deserializes the JSON-formatted string to a Card object.
        Note: This method assumes the JSON string is in the correct format.
        """
        data = json.loads(json_str)
        return Ice()


class BackpackItem:
    Ice or Fish
