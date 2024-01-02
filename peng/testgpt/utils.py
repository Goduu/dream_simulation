from typing import Dict, List, Tuple, Union

from classes import Hexagon, Penguin, Player
from constants import get_start_point_direction_possible_coordinates
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
    return (q, r, s)


def coordinate_available(
    board: List[Hexagon], players: List[Player], coordinates: Tuple[int, int, int]
) -> bool:
    """
    Check if the coordinates are available in the board
    and there is no ice block in the hexagon.
    If there is an collision with a penguin, check if the penguin can move to another hexagon.
    
    Params:
    board: List of hexagons
    coordinates: Coordinates to check
    
    Returns:
    True if the coordinates are available, False otherwise
    """
    for hexagon in board:
        if hexagon.get_coordinates() == coordinates:
            if not hexagon.has_ice_block:
                collided_penguin = check_hexagon_has_penguin(hexagon.get_coordinates(), players)
                if collided_penguin:
                    available_adjacent_hexagons = get_available_adjacent_hexagons(board, collided_penguin.position, players)
                    if( not available_adjacent_hexagons):
                        return False
                return True
    return False

def check_hexagon_has_penguin(coordinates: Tuple[int, int, int], players: List[Player]) -> Union[Penguin, None]:
    """
    Check if the coordinates are available in the board
    and there is no ice block in the hexagon.
    If there is an collision with a penguin, check if the penguin can move to another hexagon.
    
    Params:
    board: List of hexagons
    coordinates: Coordinates to check
    
    Returns:
    True if the coordinates are available, False otherwise
    """
    for player in players:
        for penguin in player.penguins:
            if penguin.position == coordinates:
                return penguin
    return None

def check_for_collision(
         new_position: Tuple[int, int, int], moving_penguin: Penguin, players: List[Player]
    ) -> Union[Penguin, None]:
        """
        Checks for collision between penguins.

        Args:
            new_position (Tuple[int, int, int]): The new position to check for collision.
            moving_penguin (Penguin): The penguin that is moving.

        Returns:
            Union[Penguin, None]: The collided penguin if there is a collision, None otherwise.
        """
        # Implement logic to check for collisions with other penguins
        for player in players:
            for other_penguin in player.penguins:
                if (
                    other_penguin != moving_penguin
                    and other_penguin.position == new_position
                ):
                    return other_penguin
        return None
    

def get_start_point_surrounding_directions(
    coordinates: Tuple[int, int, int]
) -> List[str]:
    surroundings_coordinates = get_surroundings(coordinates)
    # filter surroundings_coordinates to only include coordinates that exist in outer_hexagons
    directions = []
    for s_coordinates in surroundings_coordinates:
        if s_coordinates in get_start_point_direction_possible_coordinates():
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
    """
    Calculates the direction between two hexagons.
    """
    dq, dr, ds = q2 - q1, r2 - r1, s2 - s1

    if dq == 0 and dr == 0 and ds == 0:
        return None  # No movement

    elif dq == 1 and dr == -1 and ds == 0:
        return "cs"  # Move in the q direction
    elif dq == -1 and dr == 1 and ds == 0:
        return "s"  # Move in the q direction
    elif dq == 0 and dr == 1 and ds == -1:
        return "cq"  # Move in the q direction
    elif dq == 0 and dr == -1 and ds == 1:
        return "q"  # Move in the q direction
    elif dq == -1 and dr == 0 and ds == 1:
        return "cr"  # Move in the q direction
    elif dq == 1 and dr == 0 and ds == -1:
        return "r"  # Move in the q direction

    return None  # Invalid movement


def get_adjacent_hexagons(
    board: List[Hexagon], coordinates: Tuple[int, int, int]
) -> List[Hexagon]:
    """
    Retrieves the adjacent hexagons on the board for a given coordinate.
    """
    surroundings = get_surroundings(coordinates)
    adjacent_hexagons: List[Hexagon] = []
    for surrounding_coordinates in surroundings:
        for hexagon in board:
            if hexagon.get_coordinates() == surrounding_coordinates:
                adjacent_hexagons.append(hexagon)
    return adjacent_hexagons


def get_available_adjacent_hexagons(
    board: List[Hexagon], coordinates: Tuple[int, int, int], players: List[Player]
) -> List[Hexagon]:
    """
    Retrieves the available adjacent hexagons for a given hexagon.

    This function takes a hexagon coordinate as input and returns a list of hexagons
    that are adjacent to it and are not blocked.

    Parameters:
    board List[Hexagon]: The board hexagons
    coordinates Tuple[int, int, int]: The coordinates of the hexagon to check
    players List[Player]: The list of players

    Returns:
    List[Hexagon]: A list of available adjacent hexagons.
    """
    adjacent_hexagons = get_adjacent_hexagons(board, coordinates)
    for hexagon in adjacent_hexagons:
        if hexagon.has_ice_block:
            adjacent_hexagons.remove(hexagon)
        else:
            for player in players:
                for penguin in player.penguins:
                    if (
                        penguin.position == hexagon.get_coordinates()
                        and hexagon in adjacent_hexagons
                    ):
                        adjacent_hexagons.remove(hexagon)

    return adjacent_hexagons


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
