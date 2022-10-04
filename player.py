from typing import List
from hex import Hex


class Player:

    def __init__(self, name: str, start_point: Hex, cubes: int,
                 material: int) -> None:
        self.name = name
        self.start_point = start_point
        self.occupied_coordinates: List[Hex] = [start_point]
        self.cubes = cubes
        self.material = material

    def __repr__(self):
        return f"<Player \n name:{self.name}  \n start_point:{self.start_point} \n occupied_coordinates:{self.occupied_coordinates}  \n cubes:{self.cubes}  >"