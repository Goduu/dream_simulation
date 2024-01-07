# Coordinates for the outer hexagons
from enum import Enum
import random

from classes.backpack_item import FishType


outer_hexagons_coordinates = [
    (1, -1, 0),
    (1, 0, -1),
    (0, 1, -1),
    (-1, 1, 0),
    (-1, 0, 1),
    (0, -1, 1),
]

# Coordinates for the second outer hexagons
second_outer_hexagons_coordinates = [
    (2, -2, 0),
    (2, -1, -1),
    (1, 1, -2),
    (-1, 2, -1),
    (-2, 1, 1),
    (-1, -1, 2),
    (1, -2, 1),
    (0, 2, -2),
    (-2, 0, 2),
    (2, 0, -2),
    (-2, 2, 0),
    (0, -2, 2),
]


def get_outer_hexagons_coordinates():
    return outer_hexagons_coordinates


def get_start_point_direction_possible_coordinates():
    possible_coordinates = outer_hexagons_coordinates.copy()
    possible_coordinates.extend(
        [(1, -2, 1), (2, -1, -1), (1, 1, -2), (-1, 2, -1), (-2, 1, 1), (-1, -1, 2)]
    )
    return possible_coordinates


def get_all_coordinates():
    return outer_hexagons_coordinates + second_outer_hexagons_coordinates + [(0, 0, 0)]


def get_second_outer_hexagons_coordinates():
    return second_outer_hexagons_coordinates


fish_tiles = [
    {"type": FishType.A, "quantity": 1, "probability": 1},
    {"type": FishType.A, "quantity": 2, "probability": 2},
    {"type": FishType.A, "quantity": 3, "probability": 1},
    {"type": FishType.B, "quantity": 1, "probability": 1},
    {"type": FishType.B, "quantity": 2, "probability": 2},
    {"type": FishType.B, "quantity": 3, "probability": 1},
    {"type": FishType.C, "quantity": 1, "probability": 1},
    {"type": FishType.C, "quantity": 2, "probability": 2},
    {"type": FishType.C, "quantity": 3, "probability": 1},
]


# function that get one fish tile from the fish tiles list based on the probability
def get_fish_tile():
    fish_tile = random.choices(
        fish_tiles, [fish_tile["probability"] for fish_tile in fish_tiles]
    )[0]
    return fish_tile


class Dir(Enum):
    Q = "q"
    R = "r"
    S = "s"
    CQ = "cq"
    CR = "cr"
    CS = "cs"


market_size = 6


def get_market_size():
    return market_size
