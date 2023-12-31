# Coordinates for the outer hexagons
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


def get_second_outer_hexagons_coordinates():
    return second_outer_hexagons_coordinates
