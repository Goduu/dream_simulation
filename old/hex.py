from enum import Enum
from typing import List
from hex_coordinates import HexCoordinates


class HexType(Enum):
    RED = "red"
    DOUBLE_RED = "double-red"
    GREEN = "green"
    DOUBLE_GREEN = "double-green"
    BLUE = "blue"
    DOUBLE_BLUE = "double-blue"
    MATERIAL = "material"
    START = "start"


class Hex:

    def __init__(self, coordinates: HexCoordinates, type: HexType) -> None:
        self.coordinates = coordinates
        self.type = type
        self.player_occupation = []

    def __repr__(self):
        return f"<Hex \n type:{self.type}  \n player_occupation:{self.player_occupation} \n coordinates:{self.coordinates} >"

    def get_surroundings(self) -> List[HexCoordinates]:
        q = self.coordinates.q
        r = self.coordinates.r
        s = self.coordinates.s
        return (HexCoordinates(q + 1, r - 1,
                               s), HexCoordinates(q + 1, r, s - 1),
                HexCoordinates(q, r + 1,
                               s - 1), HexCoordinates(q - 1, r + 1, s),
                HexCoordinates(q - 1, r,
                               s + 1), HexCoordinates(q, r - 1, s + 1))


def get_hex_point(self, type: HexType):
    if type == HexType.RED:
        return 1 
    if type == HexType.DOUBLE_RED:
        return 2
    if type == HexType.GREEN:
        return 1 
    if type == HexType.DOUBLE_GREEN:
        return 2
    if type == HexType.BLUE:
        return 1
    if type == HexType.DOUBLE_BLUE:
        return 2
    if type == HexType.MATERIAL:
        return 0
    if type == HexType.START:
        return 0
