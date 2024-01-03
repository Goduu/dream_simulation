from typing import Dict, List, Tuple, Union

from classes import Hexagon, Penguin, Player
from constants import get_start_point_direction_possible_coordinates
from printc import MColors, printc, emojis


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
        printc(f"Invalid direction: {direction} [calculate_new_position]", MColors.FAIL)
        pass
    return (q, r, s)


def coordinate_available(
    board: List[Hexagon], players: List[Player], coordinates: Tuple[int, int, int]
) -> bool:
    """
    Check if the coordinates are available in the board
    and there is no ice block in the hexagon.
    If there is an collision with a penguin, check if the penguin can move to another hexagon.

    """
    board_hexagon = get_hexagon(board, coordinates)
    if board_hexagon is None:
        return False

    if board_hexagon.has_ice_block:
        return False

    collided_penguin = get_hexagon_penguin(board_hexagon.get_coordinates(), players)

    if collided_penguin is None:
        return True

    available_adjacent_hexagons = get_available_adjacent_hexagons(
        board, collided_penguin.position, players
    )

    if available_adjacent_hexagons != []:
        return True

    return False


def get_hexagon_penguin(
    coordinates: Tuple[int, int, int], players: List[Player]
) -> Union[Penguin, None]:
    """
    Check if the coordinates are available in the board
    and there is no ice block in the hexagon.
    If there is an collision with a penguin, check if the penguin can move to another hexagon.

    Returns:
    True if the coordinates are available, False otherwise
    """
    for player in players:
        for penguin in player.penguins:
            if penguin.position == coordinates:
                return penguin
    return None

def outside_hexagon(coordinates: Tuple[int, int, int]) -> bool:
    """
    Check if the coordinates are outside the board
    """
    q, r, s = coordinates
    return abs(q) >= 3 or abs(r) >= 3 or abs(s) >= 3

def hexagon_empty(
    board: List[Hexagon], players: List[Player], coordinates: Tuple[int, int, int]
) -> bool:
    """
    Check if the coordinates are available in the board

    Returns:
    True if the coordinates are available, False otherwise
    """
    board_hexagon = get_hexagon(board, coordinates)
    if board_hexagon is None:
        return False

    if board_hexagon.has_ice_block:
        return False

    collided_penguin = get_hexagon_penguin(board_hexagon.get_coordinates(), players)

    if collided_penguin is None:
        return True

    return False


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


def push_penguin(penguin: Penguin, new_position: Tuple[int, int, int], direction: str):
        """
        Pushes a penguin to a new position.
        """
        if(outside_hexagon(new_position)):
            printc(f"Penguin {penguin.id} is peeing pushed outside", MColors.OKCYAN)
            penguin.position = None
            penguin.direction = None
            return
        
        penguin.direction = direction
        printc(
            f"{emojis['turn']}Changing direction from penguin {penguin.id} from {penguin.direction} to {direction} to push to {new_position}",
            MColors.OKGREEN,
        )

        penguin.position = new_position
        printc(
            f"{emojis['move']}Penguin {penguin.id} pushed to {penguin.position}",
            MColors.OKGREEN,
        )
        
def get_start_point_surrounding_directions(
    coordinates: Tuple[int, int, int]
) -> List[str]:
    surroundings_coordinates = get_surroundings(coordinates)
    # filter surroundings_coordinates to only include coordinates that exist in outer_hexagons
    directions = []
    for s_coordinates in surroundings_coordinates:
        if s_coordinates in get_start_point_direction_possible_coordinates():
            direction = calculate_direction(coordinates, s_coordinates)
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


def calculate_direction(
    coordinates1: Tuple[int, int, int], coordinates2: Tuple[int, int, int]
):
    """
    Calculates the direction between two hexagons.
    """
    q1, r1, s1 = coordinates1
    q2, r2, s2 = coordinates2
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
        board_hexagon = get_hexagon(board, surrounding_coordinates)
        if board_hexagon is not None:
            adjacent_hexagons.append(board_hexagon)
    return adjacent_hexagons


def get_available_adjacent_hexagons(
    board: List[Hexagon], coordinates: Tuple[int, int, int], players: List[Player]
) -> List[Hexagon]:
    """
    Retrieves the available adjacent hexagons for a given hexagon.
    No ice blocks or penguins are allowed in the adjacent hexagons.

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
    """
    Returns the board hexagon for a given coordinate.
    """
    for hexagon in board:
        if hexagon.get_coordinates() == coordinates:
            return hexagon
    return None
