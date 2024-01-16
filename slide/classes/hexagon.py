"""
Represents a board hexagon. 
"""
from classes.backpack_item import FishType


class Hexagon:
    """
    Represents a hexagon on the game board.

    Attributes:
    position (tuple): The hexagon's position on the board.
    fish (int): The number of fish on the hexagon.
    ice (bool): Whether the hexagon is covered in ice.
    """

    def __init__(self, q: int, r: int, s: int, fish_quantity: int, fish_type: FishType):
        self.q: int = q
        self.r: int = r
        self.s: int = s
        self.fish_quantity: int = fish_quantity
        self.fish_type: FishType = fish_type
        self.has_ice_block: bool = False

    def get_coordinates(self):
        return (self.q, self.r, self.s)
