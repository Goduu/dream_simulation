
import random
from typing import List
from xmlrpc.client import boolean
from board import Board
from functions import get_next_tile_coords_after_push, play_log
from hex_coordinates import HexCoordinates
from player import Player, PlayerSkill, PlayerSkillType, Hex
from action_functions import use_reset_skill


class MovPossibility:
    def __init__(self, from_hex: Hex, target_hex: Hex, with_skill) -> None:
        self.from_hex = from_hex
        self.target_hex = target_hex
        self.with_skill = with_skill


class MovPossible:

    def __init__(self) -> None:
        self.is_possible = False
        self.with_skill = []


def movement_possible(board: Board, player: Player, coord: HexCoordinates,
                      coord_target: HexCoordinates):
    return_val = MovPossible()
    if board.hex_exists(coord_target):
        hexagon_target = board.find_hex_by_coordinates(coord_target)
        if hexagon_target.type == "start":
            return return_val
        elif hexagon_target.occupation_number == 0:
            return_val.is_possible = True
            return return_val
        else:
            return check_push_action(board, player, coord, coord_target)
    return return_val


def check_movement_possibilities(board: Board, player: Player):
    mov_possibilities: List[MovPossibility] = list()

    for occupied_hexagon in player.occupied_hexagons:
        surrounding_coordinates = occupied_hexagon.get_surroundings()
        for sur_coord in surrounding_coordinates:
            mov_possible = movement_possible(
                board, player, occupied_hexagon.coordinates, sur_coord)
            if mov_possible.is_possible:
                mov_possibility = MovPossibility(
                    from_hex=occupied_hexagon,
                    target_hex=board.find_hex_by_coordinates(sur_coord),
                    with_skill=mov_possible.with_skill)
                mov_possibilities.append(mov_possibility)

    return mov_possibilities


def check_push_action(board: Board, player: Player, coord: HexCoordinates, coord_target: HexCoordinates):
    coord_to_move_pushed_player = get_next_tile_coords_after_push(
        coord, coord_target)
    hex_to_move_pushed_player = board.find_hex_by_coordinates(
        coord_to_move_pushed_player)

    return_val = MovPossible()

    with_skill: List[PlayerSkill] = []
    if (hex_to_move_pushed_player):
        if (hex_to_move_pushed_player.occupation_number == 0):
            return_val.is_possible = True
            return return_val
        if (player.check_skill(PlayerSkillType.PUSH_ROW)):
            with_skill.append(PlayerSkillType.PUSH_ROW)
        if (player.check_skill(PlayerSkillType.RESET)):
            with_skill.append(PlayerSkillType.RESET)
        if (player.check_skill(PlayerSkillType.SWITCH)):
            with_skill.append(PlayerSkillType.SWITCH)

    else:
        if (player.check_skill(PlayerSkillType.PUSH_BORDER)):
            with_skill.append(PlayerSkillType.PUSH_BORDER)

    return_val.is_possible = len(with_skill) > 0
    return_val.with_skill = with_skill
    return return_val


def push_action(target_player, from_hex, target_hex, board):
    if (target_player and isinstance(target_player, Player)):
        push_player(pushed_player=target_player, board=board,
                    from_hex=from_hex, target_hex=target_hex)


def push_with_skill(target_player: Player, from_player: Player, target_hex: Hex, with_skill: List[PlayerSkillType]):
    chosen_skill = random.choice(with_skill)
    if (chosen_skill == PlayerSkillType.PUSH_ROW):
        return
    elif (chosen_skill == PlayerSkillType.RESET):
        simple_move(target_hex, target_player.start_point)
        from_player.use_skill(chosen_skill)
    elif (chosen_skill == PlayerSkillType.SWITCH):
        return


# can just be move if movement is possible
def mov_player(board: Board, from_hex: Hex,
               target_hex: Hex, start_hex: Hex, with_skill: List[PlayerSkillType]):
    from_player = from_hex.player_occupation
    if (from_player):
        target_player = target_hex.occupation_number and target_hex.player_occupation

        if len(with_skill) == 0:
            # push movement
            push_action(target_player, from_hex, target_hex, board)
        else:
            push_with_skill(target_player, from_player, target_hex,
                            with_skill)

        # if he is in a start point from another player
        if (start_hex.occupation_number == 0):
            simple_move(from_hex, target_hex)
        else:
            simple_move(start_hex, target_hex)
        # from_player.partialScore.add_score(target_hex)

        from_player.cubes -= 1


# def mov_player_with_skill(board: Board, from_hex: Hex,
#                           target_hex: Hex, start_hex: Hex, skill: PlayerSkillType):
#     from_player = from_hex.player_occupation
#     target_player = len(target_hex.player_occupation
#                         ) > 0 and target_hex.player_occupation

#     # push movement
#     if (target_player and isinstance(target_player, Player)):
#         if (skill == PlayerSkillType.RESET):
#             use_reset_skill(from_player=from_player,
#                             target_player=target_player, target_player_hex=target_hex)

#             target_player.partialScore.sub_score(target_hex)

#     if (start_hex.player_occupation == 0):
#         simple_move(from_hex, target_hex)
#     else:
#         simple_move(start_hex, target_hex)
#     from_player.partialScore.add_score(target_hex)

#     from_player.cubes -= 1


def simple_move(from_hexagon: Hex, target_hexagon: Hex):
    from_player: Player = from_hexagon.player_occupation

    target_hexagon.player_occupation = from_player
    target_hexagon.occupation_number += 1

    from_player.occupied_hexagons.append(target_hexagon)

    if (from_hexagon.occupation_number == 1):
        from_player.occupied_hexagons.remove(from_hexagon)
        from_hexagon.player_occupation = None
    from_hexagon.occupation_number -= 1


def push_player(pushed_player: Player, board: Board, from_hex: Hex, target_hex: Hex):
    next_hex_coords = get_next_tile_coords_after_push(
        from_hex.coordinates, target_hex.coordinates)
    next_hex = board.find_hex_by_coordinates(next_hex_coords)

    simple_move(target_hex, next_hex)

    pushed_player.partialScore.sub_score(target_hex)
    pushed_player.partialScore.add_score(next_hex)
    if (next_hex.type == "start"):
        pushed_player.cubes += 1
