from typing import List, Tuple
from classes import Card, Hexagon, Player, Penguin, Action
from constants import get_second_outer_hexagons_coordinates
from printc import MColors, printc
from utils import (
    calculate_direction,
    calculate_new_position,
    coordinate_available,
    get_adjacent_hexagons,
    get_hexagon,
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
    if penguin.direction is not None or penguin.position is None:
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
                    Action("turn", direction),
                    Action("move", i),
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
                                Action("turn", direction),
                                Action("move", i),
                                Action("drop_ice", ice_drop_position),
                            ]
                        )


def all_hexagons_available_to_move(
    position: Tuple[int, int, int],
    direction: str,
    board: List[Hexagon],
    players: List[Player],
    hexagons_to_move: int,
) -> bool:
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


def add_actions_normal_movement(
    penguin: Penguin,
    board: List[Hexagon],
    players: List[Player],
    possible_actions: List[List[Action]],
):
    """
    For every movement token left, the penguin is given a possible action to move
    in the direction it is facing and dropping ice if it has any.
    """
    if penguin.direction is not None and penguin.position is not None:
        for move_counter in range(1, penguin.movement_tokens + 1):
            if all_hexagons_available_to_move(
                penguin.position, penguin.direction, board, players, move_counter
            ):
                if penguin.ice_tokens >= 1:
                    for ice_drop_counter in range(
                        min(penguin.ice_tokens, move_counter)
                    ):
                        ice_drop_position = calculate_new_position(
                            penguin.position, penguin.direction, ice_drop_counter
                        )
                        if hexagon_empty(board, players, ice_drop_position):
                            possible_actions.append(
                                [
                                    Action("move", move_counter),
                                    Action("drop_ice", ice_drop_position),
                                ]
                            )
                possible_actions.append([Action("move", move_counter)])
            else:
                # if penguin still have movements left, go out of the board and start again
                if penguin.movement_tokens > 0:
                    possible_actions.append([Action("move_out", None)])


def add_actions_first_movement(
    penguin: Penguin,
    board: List[Hexagon],
    players: List[Player],
    possible_actions: List[List[Action]],
):
    if penguin.direction is None and penguin.position is None:
        for i in range(1, penguin.movement_tokens + 1):
            for coordinate in get_second_outer_hexagons_coordinates():
                if coordinate_available(board, players, coordinate):
                    surrounding_directions = get_start_point_surrounding_directions(
                        coordinate
                    )

                    for direction in surrounding_directions:
                        new_coordinate = calculate_new_position(
                            coordinate, direction, i
                        )
                        if coordinate_available(board, players, new_coordinate):
                            possible_actions.append(
                                [
                                    Action("start", (coordinate, direction)),
                                    Action("move", i),
                                ]
                            )


def check_penguin_can_use_card(
    penguin: Penguin, card: Card, possible_actions: List[Action]
) -> bool:
    effects = card.on_play_effect
    for effect_key in effects:
        effect_value = effects[effect_key]
        if effect_value < 0:
            if effect_key == "movement_token":
                movement_actions = [
                    action
                    for action in possible_actions
                    if action.type == "move_out" or action.type == "start"
                ]
                move_tokens = sum(
                    [
                        action.parameter
                        for action in possible_actions
                        if action.type == "move"
                    ]
                )
                if (
                    penguin.movement_tokens
                    < abs(effect_value) + movement_actions.__len__() + move_tokens
                ):
                    return False
            elif effect_key == "fishing_token":
                if penguin.fishing_tokens < abs(effect_value):
                    return False
            elif effect_key == "ice_token":
                if penguin.ice_tokens < abs(effect_value):
                    return False
            else:
                printc(f"Effect key {effect_key} not found", MColors.FAIL)
    return True


def add_play_card_actions(
    player: Player, penguin: Penguin, possible_actions: List[List[Action]]
):
    play_card_actions: List[Action] = []

    for card in player.cards:
        for actions in possible_actions or [[]]:
            if check_penguin_can_use_card(penguin, card, actions):
                actions_copy = actions.copy()
                actions_copy.append(Action("play_card", card.short_name))
                play_card_actions.append(actions_copy)

    possible_actions.extend(play_card_actions)


def get_possible_actions(
    player: Player,
    penguin: Penguin,
    board: List[Hexagon],
    card_market: List[Card],
    players: List[Player],
) -> List[List[Action]]:
    possible_actions: List[List[Action]] = []

    # Penguin Movement
    if penguin.movement_tokens > 0:
        # First penguin movement (without position or direction set)
        add_actions_first_movement(penguin, board, players, possible_actions)

        # Normal movement (with position and direction set)
        add_actions_normal_movement(penguin, board, players, possible_actions)

        # Movement after passing season (with position but no direction set)
        add_actions_after_passing_season(penguin, board, players, possible_actions)

        if possible_actions == [] and penguin.movement_tokens > 0:
            # printc all penguin properties
            printc(
                f"Penguin properties: {penguin.id}, {penguin.position}, {penguin.direction}, {penguin.movement_tokens}"
            )

    # Check if the penguin can break ice
    if penguin.position is not None:
        adjacent_hexagons = get_adjacent_hexagons(board, penguin.position)
        if adjacent_hexagons:
            for adj_hexagon in adjacent_hexagons:
                if adj_hexagon.has_ice_block:
                    possible_actions.append([Action("break_ice", adj_hexagon)])

    # Check if the penguin can buy cards
    if card_market:
        for i, card in enumerate(card_market):
            if has_enough_tokens(penguin, card.cost):
                possible_actions.append([Action("buy_card", i)])

    # Check if the penguin can play cards
    if player.cards:
        add_play_card_actions(player, penguin, possible_actions)
    # Check if the penguin can fish
    if penguin.fishing_tokens > 0:
        for actions in possible_actions:
            actions.append(Action("fishing", ""))

    return possible_actions
