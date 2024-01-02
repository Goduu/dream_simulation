from typing import List
from classes import Card, Hexagon, Player, Penguin, Action
from constants import get_second_outer_hexagons_coordinates
from utils import (
    calculate_direction,
    calculate_new_position,
    coordinate_available,
    get_adjacent_hexagons,
    get_start_point_surrounding_directions,
    has_enough_tokens,
)


def get_possible_actions(
    player: Player, penguin: Penguin, board: List[Hexagon], card_market: List[Card], players: List[Player]
) -> List[List[Action]]:
    possible_actions: List[List[Action]] = []

    # Check if the penguin can move
    if penguin.movement_tokens > 0:
        if penguin.direction is not None and penguin.position is not None:
            # for every movement token left, check if the next direction exists
            # in board if so add to possible actions
            for i in range(1, penguin.movement_tokens + 1):
                new_position = calculate_new_position(
                    penguin.position, penguin.direction, i
                )
                if coordinate_available(board, players, new_position):
                    if penguin.ice_tokens >= 1:
                        for j in range(min(penguin.ice_tokens, i)):
                            ice_drop_position = calculate_new_position(
                                penguin.position, penguin.direction, j
                            )
                            possible_actions.append(
                                [
                                    Action("move", i),
                                    Action("drop_ice", ice_drop_position),
                                ]
                            )
                    else:
                        possible_actions.append([Action("move", i)])
                else:
                    break

        # When penguin just passed season
        elif penguin.direction is None and penguin.position is not None:
            for i in range(1, penguin.movement_tokens+1):
                adjacent_hexagons = get_adjacent_hexagons(board, penguin.position)
                for hexagon in adjacent_hexagons:
                    q, r, s = hexagon.get_coordinates()
                    pos = penguin.position
                    direction = calculate_direction(pos[0], pos[1], pos[2], q, r, s)
                    actions = [Action("turn", direction), Action("move", i)]
                    possible_actions.append(actions)

        # first penguin movement
        else:
            for i in range(1, penguin.movement_tokens+1):
                for coordinate in get_second_outer_hexagons_coordinates():
                    if coordinate_available(board, players, coordinate):
                        surrounding_directions = get_start_point_surrounding_directions(
                            coordinate
                        )
                        for direction in surrounding_directions:
                            actions = [Action("start", (coordinate, direction))]
                            actions.append(Action("move", i))
                            possible_actions.append(actions)

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
        for card in player.cards:
            for action in possible_actions:
                action.append(Action("play_card", card.short_name, penguin))

    # Check if the penguin can fish
    if penguin.fishing_tokens > 0:
        for actions in possible_actions:
            actions.append(Action("fishing", ""))

    return possible_actions
