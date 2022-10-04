from typing import List
from hex import Hex


class PlayerScore:
    def __init__(self) -> None:
        self.red = 0
        self.blue = 0
        self.green = 0
        self.material = 4
        self.material_ref = 4

    def add_score(self, targetHex: Hex):
        if (targetHex.type == "red"):
            self.red += 1
            self.material -= 1
        elif (targetHex.type == "blue"):
            self.blue += 1
            self.material -= 1
        elif (targetHex.type == "green"):
            self.green += 1
            self.material -= 1
        elif (targetHex.type == "double-red"):
            self.red += 2
            self.material -= 1
        elif (targetHex.type == "double-blue"):
            self.blue += 2
            self.material -= 1
        elif (targetHex.type == "double-green"):
            self.green += 2
            self.material -= 1
        elif (targetHex.type == "load"):
            self.material = 4
    
    def sub_score(self, targetHex: Hex):
        if (targetHex.type == "red"):
            self.red -= 1
            self.material += 1
        elif (targetHex.type == "blue"):
            self.blue -= 1
            self.material += 1
        elif (targetHex.type == "green"):
            self.green -= 1
            self.material += 1
        elif (targetHex.type == "double-red"):
            self.red -= 2
            self.material += 1
        elif (targetHex.type == "double-blue"):
            self.blue -= 2
            self.material += 1
        elif (targetHex.type == "double-green"):
            self.green -= 2
            self.material += 1
        elif (targetHex.type == "reload"):
            self.material = self.material_ref

    def calculate_final_score(self):
        return self.red + self.blue + self.green
    
    def get_score_list_rgb(self):
        return (self.red, self.green, self.blue, self.material)



class Player:

    def __init__(self, name: str, start_point: Hex, cubes: int) -> None:
        self.name = name
        self.start_point = start_point
        self.occupied_hexagons: List[Hex] = [start_point]
        self.cubes = cubes
        self.score = PlayerScore()

    def __repr__(self):
        return f"<Player \n name:{self.name}  \n start_point:{self.start_point} \n occupied_coordinates:{self.occupied_hexagons}  \n cubes:{self.cubes}  >"

    