"""
Represent a card on the game.
"""
from enum import Enum
import json
from typing import Dict, List, Tuple
import uuid

from classes.backpack_item import Fish


class CardPassiveTrigger(Enum):
    """
    What would trigger the passive effect of the card.
    """

    BREAK_ICE = ("break_ice",)
    PLAY_CARD = ("play_card",)
    BUY_CARD = ("buy_card",)
    COLLIDE_PENGUIN = ("collide_penguin",)

    def __repr__(self) -> str:
        return f"{self.value}"


class CardAgent(Enum):
    """
    Who will be affected by the card.
    """

    YOURSELF = "yourself"
    OTHERS = "others"
    OTHER = "other"
    ALL = "all"

    def __repr__(self) -> str:
        return f"{self.value}"


class CardOnPlayReward(Enum):
    """
    Types from on play rewards a card can give.
    """

    FISH = ("fish",)
    ICE = ("ice",)
    MOVEMENT = ("movement",)
    FISHING = ("fishing",)
    BACKPACK = ("backpack",)
    TURN = ("turn",)

    def __repr__(self) -> str:
        return f"{self.value}"


class CardPassiveReward(Enum):
    """
    Types from passive rewards a card can give.
    """

    FISH = ("fish",)
    ICE = ("ice",)
    MOVEMENT = ("movement",)
    FISHING = ("fishing",)
    BACKPACK = ("backpack",)
    # IGNORE_COLLISION = ("ignore_collision",)

    def __repr__(self) -> str:
        return f"{self.value}"


class Card:
    """
    Represents a card in the game.
    """

    def __init__(
        self,
        short_name: str,
        cost: List[Tuple[str, int]],
        card_type: str,
        passive_effect: Dict[CardAgent, Dict[CardOnPlayReward, int]],
        on_play_effects: Dict[CardAgent, Dict[CardOnPlayReward, int]],
        description: str,
        points: int = 1,
        quantity: int = 1,
    ):
        self.id = uuid.uuid4()
        self.short_name: str = short_name
        self.cost: List[Tuple[str, int]] = cost
        self.type: str = card_type
        self.effect: str = description
        self.points: int = points
        self.passive_effect = passive_effect
        self.on_play_effect = on_play_effects
        self.quantity = quantity

    def to_json(self):
        """
        Serializes the Card object to a JSON-formatted string.
        """
        return json.dumps(
            {
                "id": str(self.id),  # Convert UUID to string
                "short_name": self.short_name,
                "cost": self._serialize_complex_attribute(self.cost),
                "type": self.type,
                "effect": self.effect,
                "points": self.points,
                "passive_effect": self._serialize_complex_attribute(
                    self.passive_effect
                ),
                "on_play_effect": self._serialize_complex_attribute(
                    self.on_play_effect
                ),
                "quantity": self.quantity,
            }
        )

    @staticmethod
    def _serialize_complex_attribute(attr):
        """
        Serializes complex attributes like dictionaries containing Enums.
        This method will convert Enums to their value for JSON serialization.
        """
        if isinstance(attr, Enum):
            return attr.value[0]
        if isinstance(attr, dict):
            return {
                key.value[0]: Card._serialize_complex_attribute(value)
                for key, value in attr.items()
            }
        if isinstance(attr, list):
            return [Card._serialize_complex_attribute(item) for item in attr]
        if isinstance(attr, tuple):
            return tuple(Card._serialize_complex_attribute(item) for item in attr)
        if isinstance(attr, Fish):
            return attr.to_json()

        return attr

    @staticmethod
    def from_json(json_str):
        """
        Deserializes the JSON-formatted string to a Card object.
        Note: This method assumes the JSON string is in the correct format.
        """
        data = json.loads(json_str)
        return Card(**data)

    def __repr__(self) -> str:
        return f"Card: {self.short_name} \
                Cost: {self.cost} \
                Passive Effect: {self.passive_effect} \
                On Play Effect: {self.on_play_effect} \
                Points: {self.points} \
                Quantity: {self.quantity}"
