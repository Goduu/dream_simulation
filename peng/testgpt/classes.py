from enum import Enum
from typing import Dict, List, Optional, Tuple

from printc import MColors, printc, emojis


class Hexagon:
    """
    Represents a hexagon on the game board.

    Attributes:
    position (tuple): The hexagon's position on the board.
    fish (int): The number of fish on the hexagon.
    ice (bool): Whether the hexagon is covered in ice.
    """

    def __init__(self, q: int, r: int, s: int, fish_quantity: int, fish_type: str):
        self.q: int = q
        self.r: int = r
        self.s: int = s
        self.fish_quantity: int = fish_quantity
        self.fish_type: str = fish_type
        self.has_ice_block: bool = False

    def get_coordinates(self):
        return (self.q, self.r, self.s)


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
        self.fish_tokens: list[
            Tuple[str, int]
        ] = []  # List of tuples representing fish type and quantity
        self.ice_tokens: int = penguin_type["ice"]
        self.backpack: list[Tuple[str, str]] = [
            ("ice", None) for _ in range(penguin_type["ice"])
        ]  # List of tuples representing item type and fish type
        self.max_backpack_slots: int = penguin_type["slots"]
        self.direction: Optional[
            str
        ] = None  # Direction in which the penguin is moving (q,r,s,cq,cr,cs)
        self.position: Optional[Tuple[int, int, int]] = None  # Hexagon coordinates
        self.cards: List[Card] = []  # List to store penguin's cards
        self.terminated = False

    def deduct_cost_tokens(self, cost: List[Tuple[str, int]]):
        """
        Deducts cost tokens from the given penguin.

        Parameters:
        cost (List[Tuple[str, int]]): A list of tuples representing the fish type and quantity to be deducted.

        Returns:
        None
        """
        # Deduct the cost tokens from the player's penguin
        for fish_type, quantity in cost:
            for fish_token in self.fish_tokens:
                if fish_token.fish_type == fish_type:
                    fish_token.quantity -= quantity
                # remove the fish_token from the backpack_slots
                for item in self.backpack:
                    if item.type == fish_type:
                        self.backpack.remove(item)
                        break

    def break_ice(self, hexagon_with_ice: Hexagon):
        """
        Breaks the ice at the given position.

        Parameters:
        position (tuple): The position of the ice to break, represented as a tuple of coordinates.

        Returns:
        None
        """
        if hexagon_with_ice and hexagon_with_ice.has_ice_block:
            self.ice_tokens += 1
            hexagon_with_ice.has_ice_block = False
        else:
            print("Hexagon does not have an ice block.")

    def reverse_direction(self):
        """
        Reverses the given direction.

        Returns:
        str: The reversed direction.
        """
        direction_map = {
            "r": "cr",
            "cr": "r",
            "s": "cs",
            "cs": "s",
            "q": "cq",
            "cq": "q",
        }
        self.direction = direction_map.get(self.direction, self.direction)

    def move_penguin(self, new_position: Tuple[int, int, int]):
        """
        Moves a penguin to a new position.

        Args:
            penguin (Penguin): The penguin to move.
            new_position (Tuple[int, int, int]): The new position to move the penguin to.
        """
        self.position = new_position
        self.movement_tokens -= 1
        printc(
            f"{emojis['move']}Penguin {self.id} moved to {self.position}",
            MColors.OKGREEN,
        )

    def move_to_start_point(self, position, direction):
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
            f"{emojis['start']}Penguin {self.id} moved in the board to {self.position} direction {self.direction}",
            MColors.OKGREEN,
        )


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
        on_play_effects: Dict,
        description: str,
        points: int = 0,
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
    
    def __repr__(self) -> str:
        return f"{self.short_name} Cost: {self.cost}"


all_cards = [
    Card(
        short_name="BreakIceGainFish",
        cost=[("A", 2)],
        card_type="Passive",
        passive_effect="break_ice",
        on_play_effects={},
        description="When breaking an ice, get one fish token",
        points=1,
    ),
    Card(
        short_name="BreakIceGainMove",
        cost=[("A", 2)],
        card_type="Passive",
        passive_effect="break_ice",
        on_play_effects={},
        description="When breaking an ice, get one movement",
        points=1,
    ),
    Card(
        short_name="GainFishOnCardPlay",
        cost=[("A", 2)],
        card_type="Fishing",
        passive_effect="play_card",
        on_play_effects={},
        description="When playing a card to this penguin, get one fish token",
        points=1,
    ),
    Card(
        short_name="BreakIceGainFishing",
        cost=[("C", 2)],
        card_type="Passive",
        passive_effect="break_ice",
        on_play_effects={},
        description="When breaking an ice, get one fishing token",
        points=1,
    ),
    Card(
        short_name="ChangeDirectionOnCollision",
        cost=[("C", 2)],
        card_type="Passive",
        passive_effect="collide_penguin",
        on_play_effects={},
        description="When colliding with a penguin, change your penguin direction",
        points=1,
    ),
    Card(
        short_name="LoseMoveGainIce",
        cost=[("A", 2)],
        card_type="Movement",
        passive_effect="",
        on_play_effects={"movement_token": -1, "ice_token": 2},
        description="Lose one movement to get two ice tokens",
        points=1,
    ),
    Card(
        short_name="LoseIceGainFishing",
        cost=[("B", 2)],
        card_type="Fishing",
        passive_effect="",
        on_play_effects={"ice_token": 2, "fishing_token": 1},
        description="Lose two ice to get one fishing token",
        points=1,
    ),
    Card(
        short_name="LoseMoveGainFishing",
        cost=[("A", 2)],
        card_type="Movement",
        passive_effect="",
        on_play_effects={"movement_token": -1, "fishing_token": 1},
        description="Lose one movement to get one fishing token",
        points=1,
    ),
    Card(
        short_name="LoseFishingGainMove",
        cost=[("B", 2)],
        card_type="Fishing",
        passive_effect="",
        on_play_effects={"fishing_token": -1, "movement_token": 1},
        description="Lose one fishing to get one movement token",
        points=1,
    ),
    Card(
        short_name="ChangeDirection",
        cost=[("A", 2)],
        card_type="Movement",
        passive_effect="",
        on_play_effects={},
        description="Change penguin direction",
        points=1,
    ),
    Card(
        short_name="LoseIceGainFish",
        cost=[("A", 2)],
        card_type="Fishing",
        passive_effect="",
        on_play_effects={"ice_token": -1, "fish_token": 1},
        description="Lose one ice and get one fish token",
        points=1,
    ),
    Card(
        short_name="IgnoreCollisionOnce",
        cost=[("C", 2)],
        card_type="Special",
        passive_effect="",
        on_play_effects={},
        description="Ignore colliding once",
        points=1,
    ),
    Card(
        short_name="PlaceIceOnPenguins",
        cost=[("C", 2)],
        card_type="Special",
        passive_effect="",
        on_play_effects={},
        description="Every player gets one ice token and needs to place it on one of its penguins",
        points=1,
    ),
    Card(
        short_name="ChooseFishForYouAndOthers",
        cost=[("A", 2)],
        passive_effect="",
        card_type="Fishing",
        on_play_effects={},
        description="Get two fish tokens of your choice, the other players get one of the same",
        points=1,
    ),
    Card(
        short_name="DiscardFishForOthers",
        cost=[("C", 2)],
        card_type="Special",
        passive_effect="",
        on_play_effects={},
        description="Every other player should discard a fish token",
        points=1,
    ),
    Card(
        short_name="GainMovesOnce",
        cost=[("A", 2)],
        card_type="Movement",
        passive_effect="",
        on_play_effects={"movement_token": 2},
        description="Get two movement tokens once",
        points=1,
    ),
    Card(
        short_name="GainFishingOnce",
        cost=[("B", 2)],
        card_type="Fishing",
        passive_effect="",
        on_play_effects={"fishing_token": 2},
        description="Get two fishing tokens once",
        points=1,
    ),
    Card(
        short_name="ExpandBackpack",
        cost=[("C", 2)],
        card_type="Special",
        passive_effect="",
        on_play_effects={"backpack": 2},
        description="Expand its backpack slots by 2",
        points=1,
    ),
]


def get_all_cards():
    return all_cards


# Constants for penguin types
BIG_PENGUIN = {"name": "BIG", "movement": 2, "fishing": 2, "ice": 4, "slots": 8}
MEDIUM_PENGUIN = {"name": "MED", "movement": 3, "fishing": 3, "ice": 2, "slots": 3}
SMALL_PENGUIN = {"name": "SMALL", "movement": 4, "fishing": 2, "ice": 1, "slots": 6}


class Player:
    """
    Represents a player in the game.

    Attributes:
    name (str): The player's name.
    hand (list of Card): The cards in the player's hand.
    penguins (list of Penguin): The player's penguins.
    tokens (int): The number of tokens the player has.
    """

    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.color: str = None
        self.penguins: List[Penguin] = [
            Penguin(BIG_PENGUIN, player_id),
            Penguin(MEDIUM_PENGUIN, player_id),
            Penguin(SMALL_PENGUIN, player_id),
        ]
        self.cards: List[Card] = []  # List to store player's cards
        self.terminated = False
        self.season = 0
        # Other attributes as needed

    def get_card(self, card_short_name: str) -> bool:
        """
        Retrieves the card of the given player.

        Parameters:
        card_short_name (str): The short name of the card to retrieve.

        Returns:
        Card or None: The card with the given short name, or None if not found.
        """
        # Check if the player has the card
        for card in self.cards:
            if card.short_name == card_short_name:
                return card
        return None

    def play_card(self, penguin: Penguin, card_short_name: str):
        """
        Plays a card from the given player's hand.

        Parameters:
        player (Player): The player who is playing the card.
        card (Card): The card to be played.

        Returns:
        None
        """
        # Check if the player has the card
        card: Card = self.get_card(card_short_name)

        if card is not None:
            # Remove the card from the player's hand
            self.cards.remove(card)

            # Add the card to the penguin's cards
            penguin.cards.append(card)

            # Check if the card has an effect
            if "ice_token" in card.on_play_effect:
                penguin.ice_tokens += card.on_play_effect["ice_token"]
                penguin.backpack.append(("ice", "ice"))
            if "movement_token" in card.on_play_effect:
                penguin.movement_tokens += card.on_play_effect["movement_token"]
            if "fishing_token" in card.on_play_effect:
                penguin.fishing_tokens += card.on_play_effect["fishing_token"]
            if "fish_token" in card.on_play_effect:
                penguin.fish_tokens.append(("A", card.on_play_effect["fish_token"]))
                penguin.backpack.append(("fish", "A"))
            if "backpack" in card.on_play_effect:
                penguin.max_backpack_slots += card.on_play_effect["backpack"]

    def all_penguins_terminated(self):
        """
        Checks if all penguins of a player are terminated.

        Returns:
            bool: True if all penguins are terminated, False otherwise.
        """
        for penguin in self.penguins:
            if not penguin.terminated:
                return False
        return True

    # function that print using the function printc all the penguins properties from the player in a table format
    def print_penguins(self):
        printc(f"Player {self.player_id} penguins:", MColors.OKBLUE)
        printc(
            f"{'Penguin':<10}{'Position':<10}{'Direction':<10}{'Movement':<10}{'Fishing':<10}{'Ice':<10}{'Backpack':<40}{'Cards':<10}",
            MColors.OKBLUE,
        )
        for penguin in self.penguins:
            q, r, s = penguin.position if penguin.position else ("-", "-", "-")
            direction = penguin.direction or "-"
            printc(
                f"{penguin.id:<10}{q},{r},{s:<10}{direction:<10}{penguin.movement_tokens:<10}{penguin.fishing_tokens:<10}{penguin.ice_tokens:<10}{f'{[item[0] for item in penguin.backpack]}':<40}{[card.short_name for card in penguin.cards]}",
                MColors.OKBLUE,
            )


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
    DROP_ICE = "drop_ice"
    BUY_CARD = "buy_card"
    PLAY_CARD = "play_card"
    BREAK_ICE = "break_ice"
    FISHING = "fishing"
    TURN = "turn"
    MOVE_OUT = "move_out"


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
