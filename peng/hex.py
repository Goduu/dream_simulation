from hex_coordinates import HexCoordinates
from typing import List
from enum import Enum

class HexType(Enum):
    R1 = "r1"
    R2 = "r2"
    R3 = "r3"
    R4 = "r4"
    BORDER = "border"
    
class Hex:
    min = -2
    max = 2
    
    def __init__(self, id, coordinates: HexCoordinates, type: HexType, border=False) -> None:
        self.id = id
        self.coordinates = coordinates
        self.type = type
        self.penguin_occupation = False
        self.iced = False
        self.border = border

    def __repr__(self):
        return f"<Hex \n type:{self.type}  \n penguin_occupation:{self.penguin_occupation} \n coordinates:{self.coordinates} >"

    def __eq__(self, other):
        if isinstance(other, Hex):
            return self.coordinates == other.coordinates
        return NotImplemented
        
    def get_surroundings(self) -> List[HexCoordinates]:
        q = self.coordinates.q
        r = self.coordinates.r
        s = self.coordinates.s
        surroundings = [HexCoordinates(q + 1, r - 1, s),
                HexCoordinates(q + 1, r, s - 1),
                HexCoordinates(q, r + 1, s - 1),
                HexCoordinates(q - 1, r + 1, s),
                HexCoordinates(q - 1, r,s + 1),
                HexCoordinates(q, r - 1, s + 1)
                ]
        return filter_out_of_bound_coordinates(surroundings)

def filter_out_of_bound_coordinates(coordinates_list: List[HexCoordinates]) -> List[HexCoordinates]:
    filtered_list = []
    for coordinates in coordinates_list:
        q, r, s = coordinates.q, coordinates.r, coordinates.s
        if q >= Hex.min and q <= Hex.max and r >= Hex.min and r <= Hex.max and s >= Hex.min and s <= Hex.max:
            filtered_list.append(coordinates)
        # else:
        #     print(q,r,s)
    return filtered_list

def find_hex_by_coordinates(hexes: List[Hex], coordinates: HexCoordinates):
        for h in hexes:
            if (h.coordinates == coordinates):
                return h