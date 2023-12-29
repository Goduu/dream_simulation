
from hex_coordinates import HexCoordinates
from hex import Hex


class MovPossibility:
    def __init__(self, from_hex: Hex, target_hex: Hex, with_skill) -> None:
        self.from_hex = from_hex
        self.target_hex = target_hex
        self.with_skill = with_skill


class MovPossible:
    def __init__(self) -> None:
        self.is_possible = False
        self.with_skill = []
        

# def movement_possible(board: Board, player: Player, coord: HexCoordinates,
#                       coord_target: HexCoordinates):
#     return_val = MovPossible()
#     if board.hex_exists(coord_target):
#         hexagon_target = board.find_hex_by_coordinates(coord_target)
#         if hexagon_target.type == "start":
#             return return_val
#         elif hexagon_target.occupation_number == 0:
#             return_val.is_possible = True
#             return return_val
#         else:
#             return check_push_action(board, player, coord, coord_target)
#     return return_val


# def check_movement_possibilities(board: Board, player: Player):
#     mov_possibilities: List[MovPossibility] = list()

#     for occupied_hexagon in player.occupied_hexagons:
#         surrounding_coordinates = occupied_hexagon.get_surroundings()
#         for sur_coord in surrounding_coordinates:
#             mov_possible = movement_possible(
#                 board, player, occupied_hexagon.coordinates, sur_coord)
#             if mov_possible.is_possible:
#                 mov_possibility = MovPossibility(
#                     from_hex=occupied_hexagon,
#                     target_hex=board.find_hex_by_coordinates(sur_coord),
#                     with_skill=mov_possible.with_skill)
#                 mov_possibilities.append(mov_possibility)

#     movs_without_skill = [
#         mov for mov in mov_possibilities if len(mov.with_skill) == 0]
#     if (len(movs_without_skill) == 0 and  len(mov_possibilities) > 0 ):
#         return mov_possibilities
#     else:
#         return movs_without_skill



def get_next_hex_coord(coord: HexCoordinates,
                                    coord_target: HexCoordinates):
    return coord_target + (coord_target - coord)



    

