"""
Get Possible Actions given a penguin return all possible actions that this penguin
can take on his turn.
"""
from typing import List, Tuple
from classes.card import Card, CardAgent
from classes.card import CardOnPlayReward
from classes.penguin import Penguin
from classes.hexagon import Hexagon
from classes.player import Player
from classes.action import Action, ActionType

from constants import Dir, get_second_outer_hexagons_coordinates
from printc import MColors, printc
from utils import (
    calculate_direction,
    calculate_new_position,
    coordinate_available,
    get_adjacent_hexagons,
    get_start_point_surrounding_directions,
    has_enough_tokens,
    hexagon_empty,
)


def add_actions_after_passing_season(
    penguin: Penguin,
    board: List[Hexagon],
    players: List[Player],
    possible_actions: List[List[Action]],
):
    """
    Add actions for the first movement of a penguin after passing season.
    """
    if penguin.position is None:
        return

    for i in range(1, penguin.movement_tokens + 1):
        adjacent_hexagons = get_adjacent_hexagons(board, penguin.position)
        for hexagon in adjacent_hexagons:
            hexagon_coordinates = hexagon.get_coordinates()
            direction = calculate_direction(penguin.position, hexagon_coordinates)

            all_hexagons_available = all_hexagons_available_to_move(
                penguin.position, direction, board, players, i
            )

            if not all_hexagons_available:
                return

            possible_actions.append(
                [
                    Action(ActionType.TURN, direction),
                    Action(ActionType.MOVE, i),
                ]
            )

            if penguin.ice_tokens >= 1:
                for j in range(min(penguin.ice_tokens, i)):
                    ice_drop_position = calculate_new_position(
                        penguin.position, direction, j
                    )
                    if hexagon_empty(board, players, ice_drop_position):
                        possible_actions.append(
                            [
                                Action(ActionType.TURN, direction),
                                Action(ActionType.MOVE, i),
                                Action(ActionType.DROP_ICE, ice_drop_position),
                            ]
                        )


def all_hexagons_available_to_move(
    position: Tuple[int, int, int],
    direction: Dir,
    board: List[Hexagon],
    players: List[Player],
    hexagons_to_move: int,
) -> bool:
    """
    Return True if all hexagons in a move range are available to move.
    """
    all_hexagons_available = True
    for i in range(1, hexagons_to_move + 1):
        new_position = calculate_new_position(position, direction, i)
        if i == hexagons_to_move:
            if coordinate_available(board, players, new_position) is False:
                return False
        else:
            if hexagon_empty(board, players, new_position) is False:
                return False

    return all_hexagons_available

def add_actions_first_movement(
    penguin: Penguin,
    board: List[Hexagon],
    players: List[Player],
    possible_actions: List[List[Action]],
):
    """
    Add actions for the first movement of a penguin. It happens when it is out of the board.
    """
    if penguin.direction is not None or penguin.position is not None:
        return

    for i in range(1, penguin.movement_tokens + 1):
        for coordinate in get_second_outer_hexagons_coordinates():
            if coordinate_available(board, players, coordinate):
                surrounding_directions = get_start_point_surrounding_directions(
                    coordinate
                )

                for direction in surrounding_directions:
                    new_coordinate = calculate_new_position(coordinate, direction, i)
                    if coordinate_available(board, players, new_coordinate):
                        possible_actions.append(
                            [
                                Action(ActionType.START, (coordinate, direction)),
                                Action(ActionType.MOVE, i),
                            ]
                        )


def check_penguin_can_use_card(
    penguin: Penguin, card: Card, possible_actions: List[Action]
) -> bool:
    """
    Returns True if penguin can use the card.
    """
    your_effects = (
        card.on_play_effect[CardAgent.YOURSELF]
        if CardAgent.YOURSELF in card.on_play_effect
        else {}
    )
    all_effects = (
        card.on_play_effect[CardAgent.ALL]
        if CardAgent.ALL in card.on_play_effect
        else {}
    )
    # merge both effects
    effects = {**your_effects, **all_effects}
    for effect_key in effects:
        effect_value = effects[effect_key]
        if effect_value < 0:
            if effect_key == CardOnPlayReward.MOVEMENT:
                movement_actions = [
                    action
                    for action in possible_actions
                    if action.type == ActionType.MOVE_OUT
                    or action.type == ActionType.START
                ]
                move_tokens = sum(
                    [
                        action.parameter
                        for action in possible_actions
                        if action.type == ActionType.MOVE
                    ]
                )
                if (
                    penguin.movement_tokens
                    < abs(effect_value) + movement_actions.__len__() + move_tokens
                ):
                    return False
            elif effect_key == CardOnPlayReward.FISHING:
                if penguin.fishing_tokens < abs(effect_value):
                    return False
            elif effect_key == CardOnPlayReward.ICE:
                if penguin.ice_tokens < abs(effect_value):
                    return False
            elif effect_key == CardOnPlayReward.FISH:
                if len(penguin.backpack) >= penguin.max_backpack_slots:
                    return False
            else:
                printc(f"Effect key {effect_key} not found", MColors.FAIL)
    return True


def add_play_card_actions(
    player: Player, penguin: Penguin, possible_actions: List[List[Action]]
):
    """
    Add play card action to possible actions if the player can use the card.
    """
    play_card_actions: List[Action] = []

    for card in player.cards:
        for actions in possible_actions or [[]]:
            if check_penguin_can_use_card(penguin, card, actions):
                actions_copy = actions.copy()
                actions_copy.append(Action(ActionType.PLAY_CARD, card.short_name))
                play_card_actions.append(actions_copy)

    possible_actions.extend(play_card_actions)


def add_fishing_actions(penguin: Penguin, possible_actions: List[List[Action]]):
    """
    Add fishing action to possible actions if the penguin has fishing tokens left.
    """
    if len(penguin.backpack) < penguin.max_backpack_slots:
        for actions in possible_actions:
            actions.append(Action(ActionType.FISHING, None))


def add_pass_season_action(player: Player, possible_actions: List[Action]):
    """
    Add pass season action to possible actions if the player has
    no penguins left with possible actions.
    """
    if player.season >= 3 or len(possible_actions) != 0:
        return

    possible_actions.append([Action(ActionType.PASS_SEASON, None)])


def add_buy_card_action(
    penguin: Penguin, possible_actions: List[List[Action]], card_market: List[Card]
):
    """
    Add buy card action to possible actions if the penguin has enough tokens.
    """
    for i, card in enumerate(card_market):
        if has_enough_tokens(penguin, card.cost):
            for actions in possible_actions:
                actions.append(Action(ActionType.BUY_CARD, i))
            if len(possible_actions) == 0:
                possible_actions.append([Action(ActionType.BUY_CARD, i)])


def get_possible_actions(
    player: Player,
    penguin: Penguin,
    board: List[Hexagon],
    card_market: List[Card],
    players: List[Player],
) -> List[List[Action]]:
    """
    Returns an array of possible actions for a penguin.
    Each action is represented as an array of actions.
    """
    possible_actions: List[List[Action]] = []
    if player.all_penguins_terminated() and player.season < 3:
        possible_actions.append([Action(ActionType.PASS_SEASON, None)])
        return possible_actions
    # Penguin Movement
    if penguin.movement_tokens > 0:
        # First penguin movement (without position or direction set)
        add_actions_first_movement(penguin, board, players, possible_actions)

        # Normal movement (with position set) 
        add_actions_after_passing_season(penguin, board, players, possible_actions)

    # Check if the penguin can break ice
    if penguin.position is not None:
        adjacent_hexagons = get_adjacent_hexagons(board, penguin.position)
        if adjacent_hexagons:
            for adj_hexagon in adjacent_hexagons:
                if adj_hexagon.has_ice_block:
                    possible_actions.append(
                        [Action(ActionType.BREAK_ICE, adj_hexagon.get_coordinates())]
                    )

    # Check if the penguin can fish
    if penguin.fishing_tokens > 0:
        add_fishing_actions(penguin, possible_actions)

    # Check if the penguin can play cards
    if player.cards:
        add_play_card_actions(player, penguin, possible_actions)

    # Check if the penguin can buy cards
    if card_market:
        add_buy_card_action(penguin, possible_actions, card_market)

    add_pass_season_action(player, possible_actions)

    return possible_actions
