
from typing import List
from functions import get_next_tile_coords_after_push, play_log
from classes import Board,Hex,HexCoordinates,Player, PlayerSkill, PlayerSkillType
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
                    "from_hex": occupied_hexagon,
                    "target_hex": board.find_hex_by_coordinates(sur_coord),
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
        if (player.check_skill(PlayerSkillType.PUSH_ROW)):
            with_skill.append(PlayerSkillType.PUSH_ROW)
        if (player.check_skill(PlayerSkillType.RESET)):
            with_skill.append(PlayerSkillType.RESET)

    return {"is_possible": len(with_skill) > 0, "with_skill": with_skill}


# can just be move if movement is possible
def mov_player(board: Board, from_hex: Hex,
               target_hex: Hex, start_hex: Hex):
    from_player = from_hex.player_occupation[0]
    target_player = len(target_hex.player_occupation
                        ) > 0 and target_hex.player_occupation[0]

    # push movement
    if (target_player and isinstance(target_player, Player)):
        push_player(pushed_player=target_player, board=board,
                    from_hex=from_hex, target_hex=target_hex)

    # if he is in a start point from another player
    if (len(start_hex.player_occupation) == 0):
        simple_move(from_hex, target_hex)
    else:
        simple_move(start_hex, target_hex)

    from_player.cubes -= 1


def mov_player_with_skill(board: Board, from_hex: Hex,
                          target_hex: Hex, start_hex: Hex, skill: PlayerSkillType):
    print('[MOVE with SKILL] - ',from_hex.player_occupation[0].name,"from", from_hex.type, "to",target_hex.type)
    from_player = from_hex.player_occupation[0]
    target_player = len(target_hex.player_occupation
                        ) > 0 and target_hex.player_occupation[0]

    # push movement
    if (target_player and isinstance(target_player, Player)):
        if (skill == PlayerSkillType.RESET):
            use_reset_skill(from_player=from_player,
                            target_player=target_player, target_player_hex=target_hex)

            target_player.partialScore.sub_score(target_hex)

    if (len(start_hex.player_occupation) == 0):
        simple_move(from_hex, target_hex)
    else:
        simple_move(start_hex, target_hex)
    from_player.partialScore.add_score(target_hex)

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
    
    if (next_hex.type == "start"):
        pushed_player.cubes += 1