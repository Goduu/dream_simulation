"""
Represents a player in the game.
"""
from typing import List
from classes.penguin import Penguin
from classes.card import Card
from classes.penguin import BIG_PENGUIN, MEDIUM_PENGUIN, SMALL_PENGUIN

from printc import MColors, printc


class Player:
    """
    Represents a player in the game.
    """

    def __init__(self, player_id: int):
        self.id = "player_" + str(player_id)
        self.player_id: int = player_id
        self.color: str = None
        self.penguins: List[Penguin] = [
            Penguin(BIG_PENGUIN, player_id),
            Penguin(MEDIUM_PENGUIN, player_id),
            Penguin(SMALL_PENGUIN, player_id),
        ]
        self.cards: List[Card] = []  # List to store player's cards
        self.terminated = False
        self.season = 1
        # Other attributes as needed

    def score(self):
        """
        Calculates the player's score
        """
        player_score = sum([card.points for card in self.cards])
        for penguin in self.penguins:
            player_score += sum([card.points for card in penguin.cards])
        return player_score

    def get_card(self, card_short_name: str) -> bool:
        """
        Retrieves the card of the given player.
        """
        # Check if the player has the card
        for card in self.cards:
            if card.short_name == card_short_name:
                return card
        return None

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

    # function that print using the function printc all the penguins properties
    # from the player in a table format
    def print_penguins(self):
        """
        Prints the penguins of the player
        """
        printc(f"Player {self.player_id} penguins:", MColors.OKBLUE)
        printc(
            f"{'Penguin':<10}{'Position':<10}{'Direction':<10}{'Movement':<10} \
            {'Fishing':<10}{'Ice':<10}{'Backpack':<40}{'Cards':<10}",
            MColors.OKBLUE,
        )
        for penguin in self.penguins:
            q, r, s = penguin.position if penguin.position else ("-", "-", "-")
            direction = penguin.direction or "-"
            printc(
                f"{penguin.id:<10}{q},{r},{s:<10}{direction:<10}{penguin.movement_tokens:<10}\
                {penguin.fishing_tokens:<10}{penguin.ice_tokens:<10}{f'{list(penguin.backpack)}':<40} \
                {[card.short_name for card in penguin.cards]}",
                MColors.OKBLUE,
            )
