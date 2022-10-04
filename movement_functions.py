
from board import Board
from functions import get_next_tile_coords_after_push, play_log
from hex import Hex
from hex_coordinates import HexCoordinates
from player import Player, PlayerSkill, PlayerSkillType
from action_functions import use_reset_skill


def movement_possible(board: Board, player: Player, coord: HexCoordinates,
                      coord_target: HexCoordinates):
    if board.hex_exists(coord_target):
        hexagon_target = board.find_hex_by_coordinates(coord_target)
        if hexagon_target.type == "start":
            return {"is_possible": False, "with_skill": []}
        elif len(hexagon_target.player_occupation) == 0:
            return {"is_possible": True, "with_skill": []}
        else:
            return check_push_action(board, player, coord, coord_target)

    return {"is_possible": False, "with_skill": []}


def check_movement_possibilities(board: Board, player: Player):
    mov_possibilities = []
    for occupied_hexagon in player.occupied_hexagons:
        surrounding_coordinates = occupied_hexagon.get_surroundings()
        for sur_coord in surrounding_coordinates:
            mov_possible = movement_possible(
                board, player, occupied_hexagon.coordinates, sur_coord)
            if mov_possible["is_possible"] is True:
                mov_possibilities.append({
                    "from_coord": occupied_hexagon.coordinates,
                    "target_coord": sur_coord,
                    "with_skill": mov_possible["with_skill"]})

    return mov_possibilities


def check_push_action(board: Board, player: Player, coord: HexCoordinates, coord_target: HexCoordinates):
    coord_to_move_pushed_player = get_next_tile_coords_after_push(
        coord, coord_target)
    hex_to_move_pushed_player = board.find_hex_by_coordinates(
        coord_to_move_pushed_player)

    with_skill = []
    if (hex_to_move_pushed_player):
        if (hex_to_move_pushed_player.player_occupation == []):
            return {"is_possible": True, "with_skill": []}
        if (player.check_skill(PlayerSkillType.PUSH)):
            with_skill.append(PlayerSkillType.PUSH)
        if (player.check_skill(PlayerSkillType.RESET)):
            with_skill.append(PlayerSkillType.RESET)

    return {"is_possible": len(with_skill) > 0, "with_skill": with_skill}


# can just be move if movement is possible
def mov_player(board: Board, from_coord: HexCoordinates,
               target_coord: HexCoordinates, start_hexagon: Hex):
    from_player = board.find_player_by_coordinates(from_coord)
    from_hexagon = board.find_hex_by_coordinates(from_coord)
    target_hexagon = board.find_hex_by_coordinates(target_coord)
    target_player = len(target_hexagon.player_occupation
                        ) > 0 and target_hexagon.player_occupation[0]

    # push movement
    if (target_player and isinstance(target_player, Player)):
        push_player(pushed_player=target_player, board=board,
                    from_hex=from_hexagon, target_hex=target_hexagon)

    # if he is in a start point from another player
    if (len(start_hexagon.player_occupation) == 0):
        simple_move(from_hexagon, target_hexagon)
    else:
        simple_move(start_hexagon, target_hexagon)
    from_player.partialScore.add_score(target_hexagon)

    from_player.cubes -= 1


def mov_player_with_skill(board: Board, from_coord: HexCoordinates,
                          target_coord: HexCoordinates, start_hexagon: Hex, skill: PlayerSkillType):
    from_player = board.find_player_by_coordinates(from_coord)
    from_hexagon = board.find_hex_by_coordinates(from_coord)
    target_hexagon = board.find_hex_by_coordinates(target_coord)
    target_player = len(target_hexagon.player_occupation
                        ) > 0 and target_hexagon.player_occupation[0]

    # push movement
    if (target_player and isinstance(target_player, Player)):
        if (skill == PlayerSkillType.RESET):
            use_reset_skill(from_player=from_player,
                            target_player=target_player, target_player_hex=target_hexagon)

            target_player.partialScore.sub_score(target_hexagon)

    if (len(start_hexagon.player_occupation) == 0):
        simple_move(from_hexagon, target_hexagon)
    else:
        simple_move(start_hexagon, target_hexagon)
    from_player.partialScore.add_score(target_hexagon)

    from_player.cubes -= 1


def simple_move(from_hexagon: Hex, target_hexagon: Hex):
    target_hexagon.player_occupation.append(from_hexagon.player_occupation[0])
    from_player: Player = from_hexagon.player_occupation[0]
    from_player.occupied_hexagons.append(target_hexagon)

    if (len(from_hexagon.player_occupation) == 1):
        from_player.occupied_hexagons.remove(from_hexagon)
    from_hexagon.player_occupation.pop()

def push_player(pushed_player: Player, board: Board, from_hex: Hex, target_hex: Hex):
    next_hex_coords = get_next_tile_coords_after_push(
        from_hex.coordinates, target_hex.coordinates)
    next_hex = board.find_hex_by_coordinates(next_hex_coords)

    simple_move(target_hex, next_hex)
    
    pushed_player.partialScore.sub_score(target_hex)
    pushed_player.partialScore.add_score(next_hex)
    if (next_hex.type == "start"):
        pushed_player.cubes += 1