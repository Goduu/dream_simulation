from typing import Dict, List, Tuple, Union

from classes.penguin import Penguin
from classes.hexagon import Hexagon
from classes.player import Player
from classes.backpack_item import BackpackItem, Fish, Ice
from classes.card import CardPassiveTrigger, CardReward
from constants import Dir, get_start_point_direction_possible_coordinates
from printc import MColors, printc, emojis


def calculate_new_position(
    current_position: Tuple[int, int, int], direction: Dir, hexagons_to_move: int
) -> Tuple[int, int, int]:
    # Implement logic to calculate the new position based on the chosen direction and hexagons to move
    q, r, s = current_position

    if direction == Dir.Q:
        r -= hexagons_to_move
        s += hexagons_to_move
    elif direction == Dir.R:
        q += hexagons_to_move
        s -= hexagons_to_move
    elif direction == Dir.S:
        q -= hexagons_to_move
        r += hexagons_to_move
    elif direction == Dir.CQ:
        r += hexagons_to_move
        s -= hexagons_to_move
    elif direction == Dir.CR:
        q -= hexagons_to_move
        s += hexagons_to_move
    elif direction == Dir.CS:
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


def move_penguin(penguin: Penguin, new_position: Tuple[int, int, int]):
    """
    Moves a penguin to a new position.

    """
    if penguin.movement_tokens <= 0:
        printc(
            f"Penguin {penguin.id} does not have enough movement tokens.", MColors.FAIL
        )
        return
    if outside_hexagon(new_position):
        printc(f"Penguin {penguin.id} is moving outside", MColors.OKCYAN)
        penguin.position = None
        penguin.direction = None
    else:
        penguin.position = new_position
        printc(
            f"{emojis['move']}Penguin {penguin.id} moved to {penguin.position}",
            MColors.OKGREEN,
        )

    penguin.movement_tokens -= 1


def push_penguin(penguin: Penguin, new_position: Tuple[int, int, int], direction: str):
    """
    Pushes a penguin to a new position.
    """
    if outside_hexagon(new_position):
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
        return Dir.CS  # Move in the q direction
    elif dq == -1 and dr == 1 and ds == 0:
        return Dir.S  # Move in the q direction
    elif dq == 0 and dr == 1 and ds == -1:
        return Dir.CQ  # Move in the q direction
    elif dq == 0 and dr == -1 and ds == 1:
        return Dir.Q  # Move in the q direction
    elif dq == -1 and dr == 0 and ds == 1:
        return Dir.CR  # Move in the q direction
    elif dq == 1 and dr == 0 and ds == -1:
        return Dir.R  # Move in the q direction

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


def has_enough_tokens(penguin: Penguin, cost: List[BackpackItem]) -> bool:
    # Check if the player has enough tokens to buy the card
    current_in_slots: Dict[BackpackItem, int] = {}
    for item in penguin.backpack:
        item_key = item.__repr__()
        current_in_slots[item_key] = current_in_slots.get(item_key, 0) + 1
    for item, quantity in cost:
        if current_in_slots.get(item.__repr__(), 0) < quantity:
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


def apply_card_passive_effects(
    penguin: Penguin, trigger: CardPassiveTrigger, board: List[Hexagon]
):
    """
    Applies the passive effects of a card to a penguin.
    """
    for card in penguin.cards:
        effect = card.passive_effect
        if trigger in effect:
            if CardReward.FISH in effect[trigger]:
                hexagon = get_hexagon(board, penguin.position)
                if hexagon is None:
                    printc(f"No hexagon found for {penguin.position}", MColors.FAIL)
                    return
                fish_type =hexagon.fish_type
                penguin.add_in_backpack(Fish(fish_type))
            elif CardReward.ICE in effect[trigger]:
                penguin.add_in_backpack(Ice())
            elif CardReward.MOVEMENT in effect[trigger]:
                penguin.movement_tokens += effect[trigger][CardReward.MOVEMENT]
            elif CardReward.FISHING in effect[trigger]:
                penguin.fishing_tokens += effect[trigger][CardReward.FISHING]


def break_ice(penguin: Penguin, coordinate: Tuple[int, int, int], board: List[Hexagon]):
    """
    Breaks the ice at the given position.

    Parameters:
    position (tuple): The position of the ice to break, represented as a tuple of coordinates.

    Returns:
    None
    """
    hexagon = get_hexagon(board, coordinate)
    if hexagon and hexagon.has_ice_block:
        penguin.ice_tokens += 1
        hexagon.has_ice_block = False
        apply_card_passive_effects(penguin, CardPassiveTrigger.BREAK_ICE, board)
    else:
        printc(f"Hexagon {coordinate} does not have an ice block.", MColors.FAIL)
