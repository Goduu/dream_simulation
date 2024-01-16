from typing import List, Optional, Tuple
from classes.backpack_item import BackpackItem, Ice
from classes.card import Card, CardPassiveTrigger
from constants import Dir

from printc import Emojis, MColors, printc, emojis

# Constants for penguin types
BIG_PENGUIN = {"name": "BIG", "movement": 2, "fishing": 2, "ice": 4, "slots": 8}
MEDIUM_PENGUIN = {"name": "MED", "movement": 3, "fishing": 3, "ice": 2, "slots": 4}
SMALL_PENGUIN = {"name": "SMALL", "movement": 4, "fishing": 2, "ice": 1, "slots": 6}


class Penguin:
    """
    Represents a penguin in the game.

    Attributes:
    position (tuple): The penguin's current position on the board.
    owner (Player): The player who owns the penguin.
    """

    def __init__(self, penguin_type: dict, player_id: int):
        self.id: int = f'p{player_id}_{penguin_type["name"]}'
        self.type = penguin_type
        self.movement_tokens: int = penguin_type["movement"]
        self.fishing_tokens: int = penguin_type["fishing"]
        self.ice_tokens: int = penguin_type["ice"]
        self.backpack: list[BackpackItem] = [
            Ice() for _ in range(penguin_type["ice"])
        ]  # List of tuples representing item type and fish type
        self.max_backpack_slots: int = penguin_type["slots"]
        self.direction: Optional[
            Dir
        ] = None  # Direction in which the penguin is moving (q,r,s,cq,cr,cs)
        self.position: Optional[Tuple[int, int, int]] = None  # Hexagon coordinates
        self.cards: List[Card] = []  # List to store penguin's cards
        self.terminated = False

    def add_in_backpack(self, item: BackpackItem):
        """
        Adds an item in the penguin's backpack.
        """
        if len(self.backpack) == self.max_backpack_slots:
            printc(f"{self.id}'s backpack is full", MColors.WARNING)
            return
        self.backpack.append(item)

    def remove_from_backpack(self, item: BackpackItem):
        """
        Removes an item from the penguin's backpack.
        """
        printc(
            f"{self.id} removing {item} from backpack {[item for item in self.backpack]}",
            MColors.OKGREEN,
        )
        if item in self.backpack:
            self.backpack.remove(item)
        else:
            printc(f"{self.id} item {item} not found in backpack", MColors.WARNING)

    def deduct_cost_tokens(self, cost: List[BackpackItem]):
        """
        Deducts cost tokens from the given penguin.
        """
        # Deduct the cost tokens from the player's penguin
        for item, quantity in cost:
            for _ in range(quantity):
                self.remove_from_backpack(item)
                break

    def reverse_direction(self):
        """
        Reverses the given direction.

        Returns:
        str: The reversed direction.
        """
        direction_map = {
            Dir.R: Dir.CR,
            Dir.CR: Dir.R,
            Dir.S: Dir.CS,
            Dir.CS: Dir.S,
            Dir.Q: Dir.CQ,
            Dir.CQ: Dir.Q,
        }
        self.direction = direction_map.get(self.direction, self.direction)

    def move_to_start_point(self, position, direction: Dir):
        """
        Moves a penguin to the start point.

        Args:
            penguin (Penguin): The penguin to move.
            position: The position to move the penguin to.
            direction: The direction of the penguin.
        """
        self.position = position
        self.direction = direction
        printc(
            f"{self.id} moved to board on {self.position} direction {self.direction}",
            MColors.OKGREEN,
            Emojis.START,
        )
