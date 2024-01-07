from typing import List
from constants import (
    Dir,
    get_all_coordinates,
    get_market_size,
    get_second_outer_hexagons_coordinates,
)
from classes.action import Action
from all_cards import get_all_cards
from utils import get_start_point_surrounding_directions

start_hexagons = get_second_outer_hexagons_coordinates()


def add_start_actions(possible_actions: List[Action]):
    for coordinate in get_second_outer_hexagons_coordinates():
        surrounding_directions = get_start_point_surrounding_directions(coordinate)
        for direction in surrounding_directions:
            possible_actions.append(
                Action("start", (coordinate, direction)),
            )


def add_move_actions(possible_actions: List[Action]):
    for i in range(10):
        possible_actions.append(
            Action("move", i),
        )
    possible_actions.append(Action("move_out", None))


def add_turn_actions(possible_actions: List[Action]):
    for i in range(6):
        possible_actions.append(
            Action("turn", i),
        )


def add_drop_ice_actions(possible_actions: List[Action]):
    for coordinate in get_all_coordinates():
        possible_actions.append(
            Action("drop_ice", coordinate),
        )


def add_break_ice_actions(possible_actions: List[Action]):
    for coordinate in get_all_coordinates():
        possible_actions.append(
            Action("break_ice", coordinate),
        )


def add_turn_actions(possible_actions: List[Action]):
    for dir in Dir:
        possible_actions.append(
            Action("turn", dir),
        )


def add_fishing_actions(possible_actions: List[Action]):
    possible_actions.append(
        Action("fishing", None),
    )


def add_play_card_actions(possible_actions: List[Action]):
    for card in get_all_cards():
        possible_actions.append(
            Action("play_card", card.short_name),
        )


def add_buy_card_actions(possible_actions: List[Action]):
    for i in range(get_market_size()):
        possible_actions.append(
            Action("buy_card", i),
        )


def add_pass_season_action(possible_actions: List[Action]):
    possible_actions.append(
        Action("pass_season", None),
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
