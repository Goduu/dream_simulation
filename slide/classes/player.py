from typing import List
from classes.penguin import Penguin
from classes.backpack_item import Fish, FishType, Ice
from classes.card import Card
from classes.penguin import BIG_PENGUIN, MEDIUM_PENGUIN, SMALL_PENGUIN

from printc import MColors, printc, emojis


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
        """
        # Check if the player has the card
        for card in self.cards:
            if card.short_name == card_short_name:
                return card
        return None

    def play_card(self, penguin: Penguin, card_short_name: str):
        """
        Plays a card from the given player's hand.
        """
        # Check if the player has the card
        card: Card = self.get_card(card_short_name)

        if card is None:
            printc(f"Player {self.player_id} does not have the card {card_short_name}.")

        # Check if the card has an effect
        if "ice_token" in card.on_play_effect:
            penguin.ice_tokens += card.on_play_effect["ice_token"]
            penguin.add_in_backpack(Ice())
        if "movement_tokens" in card.on_play_effect:
            if (
                penguin.movement_tokens <= 0
                and card.on_play_effect["movement_tokens"] < 0
            ):
                printc(
                    f"Penguin {penguin.id} does not have enough movement tokens to play card: {card_short_name}.",
                    MColors.FAIL,
                )
                return
            penguin.movement_tokens += card.on_play_effect["movement_tokens"]
        if "fishing_token" in card.on_play_effect:
            penguin.fishing_tokens += card.on_play_effect["fishing_token"]
        if "fish_token" in card.on_play_effect:
            penguin.add_in_backpack(Fish(FishType.A))
        if "backpack" in card.on_play_effect:
            penguin.max_backpack_slots += card.on_play_effect["backpack"]

        # Remove the card from the player's hand
        self.cards.remove(card)

        # Add the card to the penguin's cards
        penguin.cards.append(card)

        printc(
            f"{emojis['card']}Card {card_short_name} played to Penguin {penguin.id}.",
            MColors.OKGREEN,
        )

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
                f"{penguin.id:<10}{q},{r},{s:<10}{direction:<10}{penguin.movement_tokens:<10}{penguin.fishing_tokens:<10}{penguin.ice_tokens:<10}{f'{[item for item in penguin.backpack]}':<40}{[card.short_name for card in penguin.cards]}",
                MColors.OKBLUE,
            )
