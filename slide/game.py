"""
game.py module

This module contains the main logic for the game. It includes functions for
initializing the card market, calculating new positions, getting available
adjacent hexagons, and checking if a player has enough tokens. 
It also imports necessary classes and constants from other modules.
"""

import random
from typing import List, Tuple

from classes.card import Card
from classes.backpack_item import Fish, Ice
from classes.penguin import Penguin
from classes.hexagon import Hexagon
from classes.player import Player

from constants import (
    get_fish_tile,
    get_market_size,
    outer_hexagons_coordinates,
    second_outer_hexagons_coordinates,
    Dir,
)
from all_cards import get_all_cards
from classes.action import Action, ActionType
from card_optimization.card_metrics import CardMetrics
from possible_actions_mapping import get_action_by_index
from get_possible_actions import get_possible_actions
from printc import Emojis, printc, MColors
from utils import (
    break_ice,
    calculate_new_position,
    check_for_collision,
    get_hexagon,
    has_enough_tokens,
    hexagon_empty,
    move_penguin,
    outside_hexagon,
    play_card,
    push_penguin,
)


def initialize_card_market(cards: List[Card]) -> List[Card]:
    """
    Initializes the card market.
    """

    # Select six random cards for the card market
    market_size = get_market_size()
    card_market = random.sample(cards, market_size)

    # remove one from cards quantity
    for card in card_market:
        card.quantity -= 1

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


class SlideGame:
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

    def __init__(self, num_players: int, cards: List[Card], metrics: List[CardMetrics]):
        """
        Initializes a new instance of the FishyPenguinsGame class.
        """
        all_cards = cards or get_all_cards()
        self.metrics = metrics
        self.players: List[Player] = [
            Player(player_id) for player_id in range(num_players)
        ]
        self.current_player_index: int = (
            0  # Index of the current player in self.players
        )
        self.board: List[
            Hexagon
        ] = initialize_board()  # Function to create and return the hexagonal board
        self.card_market: List[Card] = initialize_card_market(all_cards)
        self.all_cards = all_cards
        self.round = 0
        self.max_seasons = 3
        self.cards_bought = 0
        # Other attributes and initialization as needed

    # returns True if given coordinates exists in self.board and has no ice block in it

    def check_game_over(self):
        for player in self.players:
            self.terminate_penguins_without_possible_actions(player)

        game_over = True
        for player in self.players:
            if not player.all_penguins_terminated() or player.season < self.max_seasons:
                game_over = False
        return game_over

    def terminate_penguins_without_possible_actions(self, player: Player):
        '''
        Check if penguins have actions left and terminate the ones without possible actions
        '''
        for penguin in player.penguins:
            possible_actions = get_possible_actions(
                player, penguin, self.board, self.card_market, self.players
            )

            if len(possible_actions) == 0 or not possible_actions:
                printc(
                    f"{penguin.id} has no actions available",
                    MColors.WARNING,
                )
                penguin.terminated = True

    def check_winner(self) -> List[Player]:
        player_scores = {player.id: 0 for player in self.players}
        for player in self.players:
            player_scores[player.id] += player.score()

        # calculate and return the winner, if there is a draw return None
        max_score = max(player_scores.values())
        winners = []
        for player_id, score in player_scores.items():
            if score == max_score:
                winner = next(
                    (player for player in self.players if player.id == player_id),
                    None,
                )
                winners.append(winner)

        return winners

    def all_players_terminated(self):
        """
        Checks if all players in the game are terminated.
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
                f"{player.player_id} passed to season {player.season}",
                MColors.OKCYAN,
            )
        else:
            player.terminated = True
            printc(f"{player.id} terminated", MColors.YELLOW)

    def take_action(self, player: Player, penguin: Penguin, actions, max_actions):
        current_player = self.players[self.current_player_index]
        # create a for to iterate over actions and current_player.penguins at the same time
        actions_per_penguin = [
            actions[i : i + max_actions] for i in range(0, len(actions), max_actions)
        ]
        for penguin_index, actions in enumerate(actions_per_penguin):
            penguin = current_player.penguins[penguin_index]
            for action in actions:
                action = get_action_by_index(action)
                self.handle_action(current_player, penguin, action)

        self.move_to_next_player()

    def record_cards_win(self, cards: List[Card]):
        for card in cards:
            card_metrics = next(
                (metrics for metrics in (self.metrics) if metrics.card_id == card.id),
                None,
            )
            card_metrics.record_win()

    def update_winners_card_metrics(self, winners: List[Player]):
        for winner in winners:
            self.record_cards_win(winner.cards)

            for penguin in winner.penguins:
                self.record_cards_win(penguin.cards)

    def play_turn(self):
        """
        Plays a turn in the game.

        Returns:
            bool: True if the game has ended, False otherwise.
        """

        if self.check_game_over():
            winners = self.check_winner()
            if len(winners) == 1:
                winner = winners[0]
                printc(
                    f"Player {winner} won the game with: {winner.score()}",
                    MColors.YELLOW,
                )
            else:
                # print the winners and scores
                printc(f"Its a tie! Winners:", MColors.OKGREEN)
                for winner in winners:
                    printc(
                        f"Player {winner.id} score: {winner.score()}",
                        MColors.YELLOW,
                    )
            self.update_winners_card_metrics(winners)
            printc(f"metrics:: {self.metrics}")
            printc(f"cards_bought:: {self.cards_bought}")
            return True

        current_player = self.players[self.current_player_index]

        for penguin in current_player.penguins:
            if not penguin.terminated:
                self.chose_and_handles_penguin_actions(current_player, penguin)

        # Implement logic for passing to the next season, checking for game end conditions, etc.
        # You can add more game-related logic here

        # Move to the next player's turn
        self.move_to_next_player()
        return False

    def chose_and_handles_penguin_actions(self, player: Player, penguin: Penguin):
        """
        Handles the actions for a penguin in the game.
        """
        current_player = self.players[self.current_player_index]
        printc(
            f"{current_player.player_id}'s turn for penguin {penguin.id} at {penguin.position}",
            MColors.OKGREEN,
            Emojis.NEW,
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
            self.handle_action(current_player, penguin, action)

    def handle_action(self, player: Player, penguin: Penguin, action: Action):
        """
        Handles an action for a penguin in the game.

        """
        printc(
            f"{penguin.id} Handling action: {action}",
            MColors.OKGREEN,
            Emojis.ACTION,
        )
        if action.type == ActionType.START:
            position, direction = action.parameter
            penguin.move_to_start_point(position, direction)
        elif action.type == ActionType.TURN:
            penguin.direction = action.parameter
            printc(
                f"{penguin.id} turns to direction {penguin.direction}",
                MColors.OKGREEN,
                Emojis.TURN,
            )
        elif action.type == ActionType.MOVE:
            self.handle_move_penguin(penguin, action.parameter)
        elif action.type == ActionType.MOVE_OUT:
            if penguin.movement_tokens <= 0:
                printc(
                    f"{penguin.id} does not have enough movement tokens to move out.",
                    MColors.FAIL,
                )
                return
            penguin.position = None
            penguin.direction = None
            penguin.movement_tokens -= 1
            printc(
                f"{penguin.id} moved out of the board.",
                MColors.OKGREEN,
            )
        elif action.type == ActionType.BREAK_ICE:
            break_ice(penguin, action.parameter, self.board, self.players)
            printc(
                f"{penguin.id} at {penguin.position} breaks the ice block to an adjacent hexagon.",
                MColors.OKGREEN,
            )
        elif action.type == ActionType.BUY_CARD:
            self.buy_card(player, penguin, action.parameter)
        elif action.type == ActionType.FISHING:
            self.fish(penguin)
        elif action.type == ActionType.PLAY_CARD:
            play_card(player, penguin, action.parameter, self.metrics, self.players)
        elif action.type == ActionType.DROP_ICE:
            self.drop_ice(penguin, action.parameter)
        elif action.type == ActionType.PASS_SEASON:
            self.pass_season(player)
        elif action.type == ActionType.PASS:
            pass
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
                f"{penguin.id} moving {hexagons_to_move} hexagons in direction {direction}",
                MColors.OKGREEN,
                Emojis.MOVE,
            )
            for _ in range(hexagons_to_move):
                if penguin.direction is None:
                    printc(f"{penguin.id} has no direction.", MColors.WARNING)
                    return
                if penguin.position is None:
                    printc(f"{penguin.id} has no position.", MColors.WARNING)
                    return

                new_position = calculate_new_position(penguin.position, direction, 1)

                # Check for collisions with other penguins
                collision_penguin = check_for_collision(
                    new_position, penguin, self.players
                )
                if collision_penguin:
                    self.handle_collision(penguin, collision_penguin)
                else:
                    move_penguin(penguin, new_position)

        else:
            printc(
                f"{penguin.id} don't have enough movement tokens left.",
                MColors.WARNING,
            )

    def find_direction_to_push(
        self,
        current_coordinates: Tuple[int, int, int],
        direction: Dir,
        other_penguin: Penguin = None,
    ):
        """
        Finds the next direction to push a penguin.

        Returns:
            str: The next direction to push the penguin.
        """
        # Define the order of directions
        direction_order = [
            Dir.Q,
            Dir.CS,
            Dir.R,
            Dir.CQ,
            Dir.S,
            Dir.CR,
            Dir.Q,
            Dir.CS,
            Dir.R,
            Dir.CQ,
            Dir.S,
            Dir.CR,
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
        """
        printc(
            f"Collision between penguins at {moving_penguin.id}{moving_penguin.position} and {collided_penguin.id}{collided_penguin.position}",
            MColors.OKCYAN,
            Emojis.COLLISION,
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
                f"{moving_penguin.id} (moving) wins the collision.",
                MColors.OKGREEN,
                Emojis.WIN,
            )
            new_position = calculate_new_position(
                moving_penguin.position, moving_penguin.direction, 1
            )
            move_penguin(moving_penguin, new_position)
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
                f"{collided_penguin.id} (collided) wins the collision.",
                MColors.OKGREEN,
                Emojis.WIN,
            )
            new_position = calculate_new_position(
                moving_penguin.position, direction_to_push, 1
            )
            # Collided penguin continues in the hexagon, moving penguin is moved to an adjacent empty hexagon
            move_penguin(moving_penguin, new_position)
        else:
            printc("It's a tie! Both penguins are pushed", MColors.OKGREEN)
            direction_to_push_moving = self.find_direction_to_push(
                moving_penguin.position, moving_penguin.direction, collided_penguin
            )
            printc(
                f"{moving_penguin.id} changing direction from {moving_penguin.direction} to {direction_to_push_moving}",
                MColors.OKGREEN,
                Emojis.TURN,
            )
            moving_penguin.direction = direction_to_push_moving
            self.handle_move_penguin(moving_penguin, hexagons_to_move=1)
            direction_to_push_collided = self.find_direction_to_push(
                collided_penguin.position, collided_penguin.direction, moving_penguin
            )
            collided_penguin.direction = direction_to_push_collided
            printc(
                f"{collided_penguin.id} changing direction from {collided_penguin.direction} to {direction_to_push_collided}",
                MColors.OKGREEN,
                Emojis.TURN,
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
        printc(
            f"{penguin.id} fishes at {penguin.position}.",
            MColors.OKGREEN,
            Emojis.FISHING,
        )
        hexagon = get_hexagon(self.board, penguin.position)
        if penguin.position is not None and hexagon is not None:
            # Check if the penguin is in the same hexagon as the provided hexagon

            # Add the collected fish to the penguin's backpack
            # Assuming the backpack is a list, you might need to adapt based on your implementation
            collected_fish = 0
            for _ in range(hexagon.fish_quantity):
                if len(penguin.backpack) < penguin.max_backpack_slots:
                    penguin.add_in_backpack(Fish(hexagon.fish_type))
                    collected_fish += 1

            # Update the fishing tokens of the penguin
            penguin.fishing_tokens -= 1

            printc(
                f"{penguin.id} collected {collected_fish} {hexagon.fish_type} fish.",
                MColors.OKGREEN,
                Emojis.FISHING,
            )
            fishes_let_behind = hexagon.fish_quantity - collected_fish
            if fishes_let_behind > 0:
                printc(
                    f"{penguin.id} has no space in backpack. Left {fishes_let_behind} behind.",
                    MColors.FAIL,
                )
        else:
            printc(
                f"Penguin {penguin.id} has no postion or hexagon no found {penguin.position} {hexagon}",
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
                    f"{player.player_id} does not have enough tokens to buy card {selected_card.short_name}.",
                    MColors.FAIL,
                )
                return

            # Deduct the cost tokens from the player's penguin
            penguin.deduct_cost_tokens(selected_card.cost)

            # Give the card to the player
            player.cards.append(selected_card)

            # Remove the card from the market
            self.card_market.pop(card_index)

            printc(
                f"{penguin.id} bought card {selected_card.short_name}.",
                MColors.YELLOW,
                Emojis.CARD,
            )
            self.cards_bought += 1

            # Add another random card to the market which still has at least one card left
            # filter all cards which has quantity > 0
            cards_left = list(filter(lambda card: card.quantity > 0, self.all_cards))
            if cards_left:
                new_card = random.choice(cards_left)
                printc(
                    f"Cards {new_card.short_name} added to market.",
                    MColors.OKCYAN,
                    Emojis.PLUS,
                )
                new_card.quantity -= 1
                self.card_market.append(new_card)
            else:
                printc("No cards left to add to market", MColors.WARNING)

    def drop_ice(self, penguin: Penguin, coordinates: Tuple[int, int, int]):
        """
        Drops ice at the given coordinate.
        """
        printc(
            f"{penguin.id} dropping Ice block at {coordinates}.",
            MColors.OKGREEN,
            Emojis.ICE,
        )
        # Check if the penguin has an ice block in its backpack
        if Ice() in penguin.backpack:
            if hexagon_empty(self.board, self.players, coordinates):
                # Drop the ice block in the hexagon
                hexagon = get_hexagon(self.board, coordinates)
                hexagon.has_ice_block = True

                # Remove the ice block from the penguin's backpack
                penguin.remove_from_backpack(Ice())
                penguin.ice_tokens -= 1

                printc(
                    f"{penguin.id} dropped Ice block at {coordinates}.",
                    MColors.OKGREEN,
                    Emojis.ICE,
                )
            else:
                printc("Hexagon is occupied by another penguin.", MColors.FAIL)
        else:
            printc("Penguin does not have an ice block in its backpack.", MColors.FAIL)
