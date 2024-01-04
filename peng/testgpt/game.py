"""
game.py module

This module contains the main logic for the game. It includes functions for
initializing the card market, calculating new positions, getting available
adjacent hexagons, and checking if a player has enough tokens. 
It also imports necessary classes and constants from other modules.
"""

import random
from typing import List, Tuple, Union

from classes import Card, Hexagon, Player, Penguin, get_all_cards
from constants import (
    get_fish_tile,
    outer_hexagons_coordinates,
    second_outer_hexagons_coordinates,
)
from get_possible_actions import get_possible_actions
from printc import printc, MColors, emojis
from utils import (
    calculate_new_position,
    check_for_collision,
    get_available_adjacent_hexagons,
    get_hexagon,
    has_enough_tokens,
    hexagon_empty,
    outside_hexagon,
    push_penguin,
)


def initialize_card_market() -> List[Card]:
    """
    Initializes the card market.

    This function is responsible for setting up the card market at the start of the game.
    It should create a list of Card objects that players can buy during the game.

    Returns:
    List[Card]: The list of cards in the market.
    """
    all_cards = get_all_cards()

    # Select six random cards for the card market
    card_market = random.sample(all_cards, 6)

    return card_market


def initialize_board() -> List[Hexagon]:
    """
    Initialize the board hexagons

    Returns List[Hexagons]
    """
    board = []

    # Coordinates for the center hexagon
    fish_tile = get_fish_tile()
    center_hexagon = Hexagon(
        q=0, r=0, s=0, fish_quantity=fish_tile["quantity"], fish_type=fish_tile["type"]
    )
    board.append(center_hexagon)

    for coordinates in outer_hexagons_coordinates:
        q, r, s = coordinates
        fish_tile = get_fish_tile()
        hexagon = Hexagon(
            q=q,
            r=r,
            s=s,
            fish_quantity=fish_tile["quantity"],
            fish_type=fish_tile["type"],
        )
        board.append(hexagon)

    for coordinates in second_outer_hexagons_coordinates:
        q, r, s = coordinates
        fish_tile = get_fish_tile()
        hexagon = Hexagon(
            q=q,
            r=r,
            s=s,
            fish_quantity=fish_tile["quantity"],
            fish_type=fish_tile["type"],
        )
        board.append(hexagon)

    return board


class FishyPenguinsGame:
    """
    Represents a game of Fishy Penguins.

    Args:
        num_players (int): The number of players in the game.

    Attributes:
        players (List[Player]): The list of players in the game.
        current_player_index (int): The index of the current player in the players list.
        board (List[Hexagon]): The hexagonal board of the game.
        card_market (List[Card]): The list of cards in the card market.
        round (int): The current round of the game.
        max_seasons (int): The maximum number of seasons in the game.
    """

    def __init__(self, num_players: int):
        """
        Initializes a new instance of the FishyPenguinsGame class.

        Args:
            num_players (int): The number of players in the game.
        """
        self.players: List[Player] = [
            Player(player_id) for player_id in range(num_players)
        ]
        self.current_player_index: int = (
            0  # Index of the current player in self.players
        )
        self.board: List[
            Hexagon
        ] = initialize_board()  # Function to create and return the hexagonal board
        self.card_market: List[Card] = initialize_card_market()
        self.round = 0
        self.max_seasons = 3
        # Other attributes and initialization as needed

    # returns True if given coordinates exists in self.board and has no ice block in it

    def all_players_terminated(self):
        """
        Checks if all players in the game are terminated.

        Returns:
            bool: True if all players are terminated, False otherwise.
        """
        for player in self.players:
            if not player.terminated:
                return False
        return True

    def move_to_next_player(self):
        """
        Moves the game to the next player's turn.
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.round += 1
            printc("--------------")
            printc(f"New Round: {self.round}", MColors.OKBLUE)
            printc("--------------")

    def pass_season(self, player: Player):
        """
        Passes the current season for a player.

        Args:
            player (Player): The player to pass the season for.
        """
        player.season += 1
        if player.season < self.max_seasons:
            new_penguins = []
            for penguin in player.penguins:
                player.cards.extend(penguin.cards)
                new_penguin = Penguin(penguin.type, player.player_id)
                new_penguin.position = penguin.position
                new_penguin.direction = None
                new_penguins.append(new_penguin)
            player.penguins = new_penguins

            printc(
                f"Player {player.player_id} passed to season {player.season}",
                MColors.OKCYAN,
            )
        else:
            player.terminated = True
            printc(f"Player {player.player_id} terminated", MColors.YELLOW)

    def play_turn(self):
        """
        Plays a turn in the game.

        Returns:
            bool: True if the game has ended, False otherwise.
        """

        if self.all_players_terminated():
            printc("END GAME: All players terminated", MColors.YELLOW)
            return True

        current_player = self.players[self.current_player_index]
        all_penguins_terminated = current_player.all_penguins_terminated()
        if all_penguins_terminated:
            printc(
                f"All penguins terminated for player {current_player.player_id}",
                MColors.WARNING,
            )
            self.pass_season(current_player)
            self.move_to_next_player()
            return False

        for penguin in current_player.penguins:
            if not penguin.terminated:
                self.handle_penguin_actions(current_player, penguin)

        # Implement logic for passing to the next season, checking for game end conditions, etc.
        # You can add more game-related logic here

        # Move to the next player's turn
        self.move_to_next_player()
        return False

    def handle_penguin_actions(self, player: Player, penguin: Penguin):
        """
        Handles the actions for a penguin in the game.

        Args:
            player (Player): The player who owns the penguin.
            penguin (Penguin): The penguin to handle actions for.
        """
        current_player = self.players[self.current_player_index]
        printc(
            f"Player {current_player.player_id}'s turn for penguin {penguin.id} at {penguin.position}",
            MColors.OKGREEN,
        )

        # Implement logic for player actions (move, break ice, buy card, etc.) for each penguin
        possible_actions = get_possible_actions(
            player, penguin, self.board, self.card_market, self.players
        )
        if not possible_actions:
            printc(
                f"No actions available for this penguin. Moves left: {penguin.movement_tokens}",
                MColors.WARNING,
            )
            penguin.terminated = True
            return
        actions = random.choice(possible_actions)
        for action in actions:
            if action.type == "start":
                position, direction = action.parameter
                penguin.move_to_start_point(position, direction)
            elif action.type == "turn":
                penguin.direction = action.parameter
                printc(
                    f"{emojis['turn']}Penguin {penguin.id} turns to direction {penguin.direction}",
                    MColors.OKGREEN,
                )
            elif action.type == "move":
                self.handle_move_penguin(penguin, action.parameter)
            elif action.type == "move_out":
                if penguin.movement_tokens <= 0:
                    printc(
                        f"Penguin {penguin.id} does not have enough movement tokens to move out.",
                        MColors.FAIL,
                    )
                    return
                penguin.position = None
                penguin.direction = None
                penguin.movement_tokens -= 1
                printc(
                    f"Penguin {penguin.id} moved out of the board.",
                    MColors.OKGREEN,
                )
            elif action.type == "break_ice":
                penguin.break_ice(action.parameter)
                printc(
                    f"Penguin {penguin.id} at {penguin.position} breaks the ice block to an adjacent hexagon.",
                    MColors.OKGREEN,
                )
            elif action.type == "buy_card":
                self.buy_card(current_player, penguin, action.parameter)
            elif action.type == "fishing":
                self.fish(penguin)
            elif action.type == "play_card":
                current_player.play_card(penguin, action.parameter)
            elif action.type == "drop_ice":
                self.drop_ice(penguin, action.parameter)
            else:
                printc(f"Unimplemented action: {action.type}", MColors.FAIL)

    def handle_move_penguin(self, penguin: Penguin, hexagons_to_move: int):
        """
        Handles the movement of a penguin.

        Args:
            penguin (Penguin): The penguin to move.
            hexagons_to_move (int): The number of hexagons to move the penguin.
        """

        if penguin.movement_tokens >= hexagons_to_move:
            direction = penguin.direction

            # Implement logic to update the penguin's position based on the chosen direction and hexagons to move
            printc(
                f"{emojis['move']}Penguin {penguin.id} moves {hexagons_to_move} hexagons in direction {direction}",
                MColors.OKGREEN,
            )
            for _ in range(hexagons_to_move):
                if penguin.direction is None:
                    printc(f"Penguin {penguin.id} has no direction.", MColors.WARNING)
                    return
                if penguin.position is None:
                    printc(f"Penguin {penguin.id} has no position.", MColors.WARNING)
                    return

                new_position = calculate_new_position(penguin.position, direction, 1)

                # Check for collisions with other penguins
                collision_penguin = check_for_collision(
                    new_position, penguin, self.players
                )
                if collision_penguin:
                    self.handle_collision(penguin, collision_penguin)
                else:
                    penguin.move_penguin(new_position)

        else:
            printc(
                f"Not enough movement tokens left for penguin {penguin.id}.",
                MColors.WARNING,
            )

    def find_direction_to_push(
        self,
        current_coordinates: Tuple[int, int, int],
        direction: str,
        other_penguin: Penguin = None,
    ):
        """
        Finds the next direction to push a penguin.

        Returns:
            str: The next direction to push the penguin.
        """
        # Define the order of directions
        direction_order = [
            "q",
            "cs",
            "r",
            "cq",
            "s",
            "cr",
            "q",
            "cs",
            "r",
            "cq",
            "s",
            "cr",
        ]

        # Find the index of the current direction in the order
        if direction is None:
            direction = other_penguin.direction

        current_index = direction_order.index(direction)
        for direction_option in direction_order[current_index:]:
            new_position = calculate_new_position(
                current_coordinates, direction_option, 1
            )
            is_hexagon_empty = hexagon_empty(self.board, self.players, new_position)
            is_outside_hexagon = outside_hexagon(new_position)
            if is_hexagon_empty or is_outside_hexagon:
                if direction_option != direction:
                    return direction_option

        printc(
            f"No direction found. {current_coordinates} direction: {direction}",
            MColors.WARNING,
        )
        return None

    def handle_collision(self, moving_penguin: Penguin, collided_penguin: Penguin):
        """
        Handles a collision between two penguins.

        Args:
            moving_penguin (Penguin): The penguin that is moving.
            collided_penguin (Penguin): The penguin that collided with the moving penguin.
        """
        printc(
            f"{emojis['collision']}Collision between penguins at {moving_penguin.id}{moving_penguin.position} and {collided_penguin.id}{collided_penguin.position}",
            MColors.OKCYAN,
        )

        # Check ice tokens to determine the winner
        if (
            moving_penguin.ice_tokens > collided_penguin.ice_tokens
            or collided_penguin.direction is None
        ):
            # search for an unoccupied and not ice blocked hexagon in clockwise sense and move the losing penguin
            direction_to_push = self.find_direction_to_push(
                collided_penguin.position, collided_penguin.direction, moving_penguin
            )
            printc(
                f"Moving penguin {moving_penguin.id} wins the collision.",
                MColors.OKGREEN,
            )
            new_position = calculate_new_position(
                moving_penguin.position, moving_penguin.direction, 1
            )
            moving_penguin.move_penguin(new_position)
            # Moving penguin continues in the hexagon, collided penguin is moved to an adjacent empty hexagon
            new_position = calculate_new_position(
                collided_penguin.position, direction_to_push, 1
            )
            push_penguin(collided_penguin, new_position, direction_to_push)
        elif moving_penguin.ice_tokens < collided_penguin.ice_tokens:
            direction_to_push = self.find_direction_to_push(
                moving_penguin.position, moving_penguin.direction, collided_penguin
            )
            printc(
                f"Collided penguin {collided_penguin.id} wins the collision.",
                MColors.OKGREEN,
            )
            new_position = calculate_new_position(
                moving_penguin.position, direction_to_push, 1
            )
            # Collided penguin continues in the hexagon, moving penguin is moved to an adjacent empty hexagon
            push_penguin(moving_penguin, new_position, direction_to_push)
        else:
            printc("It's a tie! Both penguins are pushed", MColors.OKGREEN)
            direction_to_push_moving = self.find_direction_to_push(
                moving_penguin.position, moving_penguin.direction, collided_penguin
            )
            printc(
                f"Changing direction from penguin {moving_penguin.id} from {moving_penguin.direction} to {direction_to_push_moving}",
                MColors.OKGREEN,
            )
            moving_penguin.direction = direction_to_push_moving
            self.handle_move_penguin(moving_penguin, hexagons_to_move=1)
            direction_to_push_collided = self.find_direction_to_push(
                collided_penguin.position, collided_penguin.direction, moving_penguin
            )
            collided_penguin.direction = direction_to_push_collided
            printc(
                f"Changing direction from penguin {collided_penguin.id} from {collided_penguin.direction} to {direction_to_push_collided}",
                MColors.OKGREEN,
            )
            self.handle_move_penguin(collided_penguin, hexagons_to_move=1)

    def fish(self, penguin: Penguin):
        """
        Fishes at the given position.

        Parameters:
        position (tuple): The position to fish at, represented as a tuple of coordinates.

        Returns:
        int: The number of fish caught.
        """
        hexagon = get_hexagon(self.board, penguin.position)
        if penguin.position is not None and hexagon is not None:
            # Check if the penguin is in the same hexagon as the provided hexagon

            # Add the collected fish to the penguin's backpack
            # Assuming the backpack is a list, you might need to adapt based on your implementation
            for _ in range(hexagon.fish_quantity):
                penguin.backpack.append(("fish", hexagon.fish_type))

            # Update the fishing tokens of the penguin
            penguin.fishing_tokens -= 1

            printc(
                f"{emojis['fishing']}{hexagon.fish_quantity} {hexagon.fish_type} fish collected by Penguin {penguin.id}.",
                MColors.OKGREEN,
            )
        else:
            printc(
                f"Penguin {penguin.id} has no postion or hexagon no found",
                MColors.WARNING,
            )

    def buy_card(self, player: Player, penguin: Penguin, card_index: int):
        """
        Buys a card for the given player.

        Parameters:
        player (Player): The player who is buying the card.
        card (Card): The card to be bought.
        """
        if 0 <= card_index < len(self.card_market):
            selected_card = self.card_market[card_index]

            # Check if the player has enough tokens to buy the card
            if not has_enough_tokens(penguin, selected_card.cost):
                printc(
                    f"Player {player.player_id} does not have enough tokens to buy card {selected_card.short_name}.",
                    MColors.FAIL,
                )

            # Deduct the cost tokens from the player's penguin
            penguin.deduct_cost_tokens(selected_card.cost)

            # Give the card to the player
            player.cards.append(selected_card)

            # Remove the card from the market
            self.card_market.pop(card_index)

            # Add another random card to the market
            all_cards = get_all_cards()
            new_card = random.choice(all_cards)
            self.card_market.append(new_card)

            printc(
                f"{emojis['plus']}{emojis['card']}Card {selected_card.short_name} bought by Penguin {penguin.id}.",
                MColors.YELLOW,
            )

    def drop_ice(self, penguin: Penguin, coordinates: Tuple[int, int, int]):
        """
        Drops ice at the given coordinate.
        """
        # Check if the penguin has an ice block in its backpack
        if ("ice", None) in penguin.backpack:
            if hexagon_empty(self.board, self.players, coordinates):
                # Drop the ice block in the hexagon
                hexagon = get_hexagon(self.board, coordinates)
                hexagon.has_ice_block = True

                # Remove the ice block from the penguin's backpack
                penguin.backpack.remove(("ice", None))
                penguin.ice_tokens -= 1

                printc(
                    f"{emojis['ice']}Ice block dropped by Penguin {penguin.id}.",
                    MColors.OKGREEN,
                )
            else:
                printc("Hexagon is occupied by another penguin.", MColors.WARNING)
        else:
            printc("Penguin does not have an ice block in its backpack.", MColors.FAIL)
