from typing import List
from constants import (
    Dir,
    get_all_coordinates,
    get_market_size,
    get_second_outer_hexagons_coordinates,
)
from classes.action import Action, ActionType
from all_cards import get_all_cards
from printc import MColors, printc
from utils import get_start_point_surrounding_directions

start_hexagons = get_second_outer_hexagons_coordinates()


def add_start_actions(possible_actions: List[Action]):
    for coordinate in get_second_outer_hexagons_coordinates():
        surrounding_directions = get_start_point_surrounding_directions(coordinate)
        for direction in surrounding_directions:
            possible_actions.append(
                Action(ActionType.START, (coordinate, direction)),
            )


def add_move_actions(possible_actions: List[Action]):
    for i in range(10):
        possible_actions.append(
            Action(ActionType.MOVE, i),
        )
    possible_actions.append(Action(ActionType.MOVE_OUT, None))


def add_turn_actions(possible_actions: List[Action]):
    for i in range(6):
        possible_actions.append(
            Action(ActionType.TURN, i),
        )


def add_drop_ice_actions(possible_actions: List[Action]):
    for coordinate in get_all_coordinates():
        possible_actions.append(
            Action(ActionType.DROP_ICE, coordinate),
        )


def add_break_ice_actions(possible_actions: List[Action]):
    for coordinate in get_all_coordinates():
        possible_actions.append(
            Action(ActionType.BREAK_ICE, coordinate),
        )


def add_turn_actions(possible_actions: List[Action]):
    for dir in Dir:
        possible_actions.append(
            Action(ActionType.TURN, dir),
        )


def add_fishing_actions(possible_actions: List[Action]):
    possible_actions.append(
        Action(ActionType.FISHING, None),
    )


def add_play_card_actions(possible_actions: List[Action]):
    for card in get_all_cards():
        possible_actions.append(
            Action(ActionType.PLAY_CARD, card.short_name),
        )


def add_buy_card_actions(possible_actions: List[Action]):
    for i in range(get_market_size()):
        possible_actions.append(
            Action(ActionType.BUY_CARD, i),
        )


def add_pass_season_action(possible_actions: List[Action]):
    possible_actions.append(
        Action(ActionType.PASS_SEASON, None),
    )


def get_possible_actions_mapping() -> List[Action]:
    possible_actions = []

    add_start_actions(possible_actions)
    add_move_actions(possible_actions)
    add_turn_actions(possible_actions)
    add_drop_ice_actions(possible_actions)
    add_break_ice_actions(possible_actions)
    add_fishing_actions(possible_actions)
    add_play_card_actions(possible_actions)
    add_buy_card_actions(possible_actions)
    add_pass_season_action(possible_actions)

    return possible_actions


def get_action_by_index(index: int):
    possible_actions = get_possible_actions_mapping()
    return possible_actions[index]


def get_action_index_by_action(action: Action):
    possible_actions = get_possible_actions_mapping()
    return possible_actions.index(action)
