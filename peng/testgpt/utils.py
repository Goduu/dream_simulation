from typing import Dict, List, Tuple

from classes import Hexagon, Penguin, Player
from constants import outer_hexagons_coordinates
from printc import MColors, printc


def calculate_new_position(
    current_position: Tuple[int, int, int], direction: str, hexagons_to_move: int
) -> Tuple[int, int, int]:
    # Implement logic to calculate the new position based on the chosen direction and hexagons to move
    q, r, s = current_position
    if direction == "q":
        r -= hexagons_to_move
        s += hexagons_to_move
    elif direction == "r":
        q += hexagons_to_move
        s -= hexagons_to_move
    elif direction == "s":
        q -= hexagons_to_move
        r += hexagons_to_move
    elif direction == "cq":
        r += hexagons_to_move
        s -= hexagons_to_move
    elif direction == "cr":
        q -= hexagons_to_move
        s += hexagons_to_move
    elif direction == "cs":
        q += hexagons_to_move
        r -= hexagons_to_move
    else:
        printc(f"Invalid direction: {direction}", MColors.FAIL)
        pass
    return q, r, s


def check_coordinates_available(
    board: List[Hexagon], coordinates: Tuple[int, int, int]
) -> bool:
    q, r, s = coordinates
    for hexagon in board:
        if hexagon.q == q and hexagon.r == r and hexagon.s == s:
            if not hexagon.has_ice_block:
                return True
    return False


def get_surrounding_direction_hexagons(
    coordinates: Tuple[int, int, int]
) -> List[Hexagon]:
    surroundings_coordinates = get_surroundings(coordinates)
    # filter surroundings_coordinates to only include coordinates that exist in outer_hexagons
    directions = []
    for s_coordinates in surroundings_coordinates:
        if s_coordinates in outer_hexagons_coordinates:
            dq, dr, ds = s_coordinates
            q, r, s = coordinates
            direction = calculate_direction(q, r, s, dq, dr, ds)
            directions.append(direction)

    return directions


def get_surroundings(coordinates: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    q, r, s = coordinates
    return [
        (q + 1, r - 1, s),
        (q + 1, r, s - 1),
        (q, r + 1, s - 1),
        (q - 1, r + 1, s),
        (q - 1, r, s + 1),
        (q, r - 1, s + 1),
    ]


def calculate_direction(q1, r1, s1, q2, r2, s2):
    dq, dr, ds = q2 - q1, r2 - r1, s2 - s1

    if dq == 0 and dr == 0 and ds == 0:
        return None  # No movement

    if dq == 1 and dr == -1 and ds == 0:
        return "cs"  # Move in the q direction
    if dq == -1 and dr == 1 and ds == 0:
        return "s"  # Move in the q direction
    if dq == 0 and dr == 1 and ds == -1:
        return "cq"  # Move in the q direction
    if dq == 0 and dr == -1 and ds == 1:
        return "q"  # Move in the q direction
    if dq == -1 and dr == 0 and ds == 1:
        return "cr"  # Move in the q direction
    if dq == 1 and dr == 0 and ds == -1:
        return "r"  # Move in the q direction

    return None  # Invalid movement


def get_valid_adjacent_hexagons(
    board: List[Hexagon], coordinates: Tuple[int, int, int]
) -> List[Hexagon]:
    surroundings = get_surroundings(coordinates)
    adjacent_hexagons: List[Hexagon] = []
    for s in surroundings:
        q, r, s = s
        for hexagon in board:
            if hexagon.get_coordinates() == (q, r, s):
                adjacent_hexagons.append(hexagon)
    return adjacent_hexagons


def get_available_adjacent_hexagons(
    board: List[Hexagon], coordinates: Tuple[int, int, int], players: List[Player]
) -> List[Hexagon]:
    valid_adjacent_hexagons = get_valid_adjacent_hexagons(board, coordinates)
    for hexagon in valid_adjacent_hexagons:
        if hexagon.has_ice_block:
            valid_adjacent_hexagons.remove(hexagon)
        else:
            for player in players:
                for penguin in player.penguins:
                    if (
                        penguin.position == hexagon.get_coordinates()
                        and hexagon in valid_adjacent_hexagons
                    ):
                        valid_adjacent_hexagons.remove(hexagon)
                        break

    return valid_adjacent_hexagons


def has_enough_tokens(penguin: Penguin, cost: List[Tuple[str, int]]) -> bool:
    # Check if the player has enough tokens to buy the card
    current_in_slots: Dict[str, int] = {}
    for fish_token in penguin.fish_tokens:
        current_in_slots[fish_token.fish_type] = (
            current_in_slots.get(fish_token.fish_type, 0) + 1
        )

    for fish_type, quantity in cost:
        if current_in_slots.get(fish_type, 0) < quantity:
            return False
    return True


def get_hexagon(board: List[Hexagon], coordinates: Tuple[int, int, int]):
    q, r, s = coordinates
    for hexagon in board:
        if hexagon.q == q and hexagon.r == r and hexagon.s == s:
            return hexagon
    return None
