from hex import Hex
from hex_coordinates import HexCoordinates
from player import Player


def get_next_tile_coords_after_push(coord: HexCoordinates,
                                    coord_target: HexCoordinates):
    return coord_target + (coord_target - coord)


def simple_move(from_hexagon: Hex, target_hexagon: Hex):
    target_hexagon.player_occupation.append(from_hexagon.player_occupation[0])
    from_hexagon.player_occupation.pop()


def get_hex_coord(hex: Hex):
    return hex.coordinates


def get_hex_color(hex: Hex):
    type = hex.type
    if type == "start":
        return ["black"]
    elif type == "load":
        return ["yellow"]
    elif type == "double-green":
        return ["lime"]
    elif type == "double-blue":
        return ["cyan"]
    elif type == "double-red":
        return ["coral"]
    return [hex.type]


def get_hex_player(hex: Hex):
    if (len(hex.player_occupation) == 0):
        return [""]
    return [
        hex.player_occupation[0].name + " " +
        str(hex.player_occupation[0].cubes)
    ]


def play_log(type,
             player: Player,
             from_hex: Hex,
             target_hex: Hex,
             target_player: Player = {}):
    if (type == "move"):
        print("[MOVE] - ", player.name, " from ", from_hex.type,
              from_hex.coordinates.q, from_hex.coordinates.r,
              from_hex.coordinates.s, " to ", target_hex.type,
              target_hex.coordinates.q, target_hex.coordinates.r,
              target_hex.coordinates.s)
    elif (type == "push"):
        print("[PUSH] - ", player.name, " pushes ", target_player.name,
              " from ", from_hex.type, from_hex.coordinates.q,
              from_hex.coordinates.r, from_hex.coordinates.s, " to ",
              target_hex.type, target_hex.coordinates.q,
              target_hex.coordinates.r, target_hex.coordinates.s)
