from typing import List
from hex_coordinates import HexCoordinates
from player import Player
from hex import Hex

should_print = False


def get_next_hex(coord: HexCoordinates,
                                    coord_target: HexCoordinates):
    return coord_target + (coord_target - coord)


def get_hex_coord(hex: Hex):
    return hex.coordinates


def get_hex_color(hex: Hex):
    type = hex.type
    if type == "start":
        return ["black"]
    elif type == "material":
        return ["yellow"]
    elif type == "double-green":
        return ["lime"]
    elif type == "double-blue":
        return ["cyan"]
    elif type == "double-red":
        return ["coral"]
    return [hex.type]


def get_hex_player(hex: Hex):
    if (hex.occupation_number == 0):
        return [""]
    return [ hex.player_occupation.name ]


def play_log(type,
             player: Player,
             from_hex: Hex,
             target_hex: Hex,
             target_player: Player = {}):
    if(should_print == False):
        return
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
