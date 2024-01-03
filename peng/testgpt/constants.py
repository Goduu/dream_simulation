# Coordinates for the outer hexagons
import random


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


def get_second_outer_hexagons_coordinates():
    return second_outer_hexagons_coordinates


fish_tiles = [
    {
        "type": "A",
        "quantity": 1,
        "probability": 1
    },
    {
        "type": "A",
        "quantity": 2,
        "probability": 2
    },
    {
        "type": "A",
        "quantity": 3,
        "probability": 1
    },
    {
        "type": "B",
        "quantity": 1,
        "probability": 1
    },
    {
        "type": "B",
        "quantity": 2,
        "probability": 2
    },
    {
        "type": "B",
        "quantity": 3,
        "probability": 1
    },
    {
        "type": "C",
        "quantity": 1,
        "probability": 1
    },
    {
        "type": "C",
        "quantity": 2,
        "probability": 2
    },
    {
        "type": "C",
        "quantity": 3,
        "probability": 1
    },
]

# function that get one fish tile from the fish tiles list based on the probability
def get_fish_tile():
    fish_tile = random.choices(fish_tiles, [fish_tile["probability"] for fish_tile in fish_tiles])[0]
    return fish_tile