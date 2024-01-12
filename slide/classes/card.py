from enum import Enum
from typing import Dict, List, Tuple


class CardPassiveTrigger(Enum):
    BREAK_ICE = ("break_ice",)
    PLAY_CARD = ("play_card",)
    BUY_CARD = ("buy_card",)
    COLLIDE_PENGUIN = ("collide_penguin",)


class CardAgent(Enum):
    YOURSELF = ("yourself",)
    OTHERS = ("others",)
    OTHER = ("other",)
    ALL = ("all",)


class CardReward(Enum):
    FISH = ("fish",)
    ICE = ("ice",)
    MOVEMENT = ("movement",)
    FISHING = ("fishing",)
    BACKPACK = ("backpack",)


class SpecialEffects(Enum):
    IGNORE_COLLISION = ("ignore_collision",)
    TURN = ("turn",)


class Card:
    """
    Represents a card in the game.

    Attributes:
    name (str): The card's name.
    cost (int): The cost to buy the card.
    effect (function): The effect of the card when played.
    """

    def __init__(
        self,
        short_name: str,
        cost: List[Tuple[str, int]],
        card_type: str,
        passive_effect: str,
        on_play_effects: Dict[CardPassiveTrigger, Dict[CardReward, int]],
        description: str,
        points: int = 1,
        quantity: int = 1,
    ):
        self.short_name: str = short_name
        self.cost: List[Tuple[str, int]] = cost
        self.type: str = card_type
        self.effect: str = description
        self.points: int = (
            points  # Points awarded to the player when the card is played
        )
        self.passive_effect = passive_effect
        self.on_play_effect = on_play_effects
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"{self.short_name} Cost: {self.cost}"
