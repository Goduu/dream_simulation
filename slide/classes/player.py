from typing import List
from classes.penguin import Penguin
from classes.backpack_item import Fish, FishType, Ice
from classes.card import Card, CardReward
from classes.penguin import BIG_PENGUIN, MEDIUM_PENGUIN, SMALL_PENGUIN

from printc import Emojis, MColors, printc, emojis


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
        self.season = 0
        # Other attributes as needed

    def score(self):
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

    def play_card(self, penguin: Penguin, card_short_name: str):
        """
        Plays a card from the given player's hand.
        """
        # Check if the player has the card
        card: Card = self.get_card(card_short_name)

        if card is None:
            printc(
                f"Player {self.player_id} does not have the card {card_short_name}.",
                MColors.FAIL,
            )
            return

        # Check if the card has an effect
        if CardReward.ICE in card.on_play_effect:
            printc(
                f"{penguin.id} on play effect: {card.on_play_effect[CardReward.ICE]} Ice",
                MColors.OKGREEN,
                Emojis.CARD,
            )
            penguin.ice_tokens += card.on_play_effect[CardReward.ICE]
            penguin.add_in_backpack(Ice())
        if CardReward.MOVEMENT in card.on_play_effect:
            printc(
                f"{penguin.id} on play effect: {card.on_play_effect[CardReward.MOVEMENT]} Movement",
                MColors.OKGREEN,
                Emojis.CARD,
            )
            if (
                penguin.movement_tokens <= 0
                and card.on_play_effect[CardReward.MOVEMENT] < 0
            ):
                printc(
                    f"Penguin {penguin.id} does not have enough movement tokens to play card: {card_short_name}.",
                    MColors.FAIL,
                )
                return
            penguin.movement_tokens += card.on_play_effect[CardReward.MOVEMENT]
        if CardReward.FISHING in card.on_play_effect:
            printc(
                f"{penguin.id} on play effect: {card.on_play_effect[CardReward.FISHING]} Fishing",
                MColors.OKGREEN,
                Emojis.CARD,
            )
            penguin.fishing_tokens += card.on_play_effect[CardReward.FISHING]
        if CardReward.FISH in card.on_play_effect:
            printc(f"{penguin.id} on play effect: 1 Fish", MColors.OKGREEN, Emojis.CARD)
            penguin.add_in_backpack(Fish(FishType.A))
        if CardReward.BACKPACK in card.on_play_effect:
            printc(
                f"{penguin.id} on play effect: {card.on_play_effect[CardReward.BACKPACK]} Backpack Slot",
                MColors.OKGREEN,
                Emojis.CARD,
            )
            penguin.max_backpack_slots += card.on_play_effect[CardReward.BACKPACK]

        # Remove the card from the player's hand
        self.cards.remove(card)

        # Add the card to the penguin's cards
        penguin.cards.append(card)

        printc(
            f"{penguin.id} played card {card_short_name}.",
            MColors.OKGREEN,
            Emojis.CARD,
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
