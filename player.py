from enum import Enum
from typing import List
from hex import Hex


class PlayerScore:
    def __init__(self, material=4) -> None:
        self.red = 0
        self.blue = 0
        self.green = 0
        self.material = material
        self.accumulator = 0

    def __repr__(self):
        return f"<Player Score \n Acc:{self.accumulator}  \n Red:{self.red}  \n Green:{self.green}  \n Blue:{self.blue}  \n Material:{self.material}  \n  >"

    def add_score(self, targetHex: Hex, account_material=False):
        if (self.material > 0):
            if (targetHex.type == "red"):
                self.red += 1
                self.accumulator += 1
                self.material -= 1 if account_material == True else 0
            elif (targetHex.type == "blue"):
                self.blue += 1
                self.accumulator += 1
                self.material -= 1 if account_material == True else 0
            elif (targetHex.type == "green"):
                self.green += 1
                self.accumulator += 1
                self.material -= 1 if account_material == True else 0
            elif (targetHex.type == "double-red"):
                self.red += 2
                self.accumulator += 2
                self.material -= 1 if account_material == True else 0
            elif (targetHex.type == "double-blue"):
                self.blue += 2
                self.accumulator += 2
                self.material -= 1 if account_material == True else 0
            elif (targetHex.type == "double-green"):
                self.green += 2
                self.accumulator += 2
                self.material -= 1 if account_material == True else 0

    def sub_score(self, targetHex: Hex):
        if (targetHex.type == "red"):
            self.red -= 1
            self.accumulator -= 1
        elif (targetHex.type == "blue"):
            self.blue -= 1
            self.accumulator -= 1
        elif (targetHex.type == "green"):
            self.green -= 1
            self.accumulator -= 1
        elif (targetHex.type == "double-red"):
            self.red -= 2
            self.accumulator -= 2
        elif (targetHex.type == "double-blue"):
            self.blue -= 2
            self.accumulator -= 2
        elif (targetHex.type == "double-green"):
            self.green -= 2
            self.accumulator -= 2

    def calculate_final_score(self):
        return self.red + self.blue + self.green

    def get_score_list_rgb(self):
        return (self.red, self.green, self.blue, self.material)


class PlayerSkillType(Enum):
    PUSH = "push"                   # Push two in a row and stay in the first hex
    PUSH_BORDER = "push-border"     # Push in empty boarder
    RESET = "reset"                 # Reset an adjacent player
    JUMP = "jump"                   # Jump a player and move to the next hex
    CUBE = "cube"                   # Get an extra cube for 1 round
    SWITCH = "switch"               # Change place with adjacent
    EXTRA_MOVE = "extra-move"       # Move one of your cubes on the board
    THROW_BEHIND = "throw-behind"   # Move someone adjacent, to a tile behind you
    RELOAD = "reload"               # Reload your white material
    CHANGE_START = "change-start"   # Change start place
    RESET_MIDDLE = "reset-middle"   # Reset a cube in the middle of 2 of yours 
    DOUBLE_MOVE = "reset-middle"    # Move 2 Hexagons without pushing 
    COEXIST = "coexist"             # You can move to another players hex without moving him  


class PlayerSkill:
    def __init__(self, type: PlayerSkillType, charges: int) -> None:
        self.type = type
        self.charges = charges



class Player:

    def __init__(self, name: str, start_point: Hex, cubes: int, skills: List[PlayerSkill]) -> None:
        self.name = name
        self.start_point = start_point
        self.occupied_hexagons: List[Hex] = [start_point]
        self.cubes = cubes
        self.partialScore = PlayerScore()
        self.score = PlayerScore()
        self.skills: List[PlayerSkill] = skills

    def __repr__(self):
        return f"<Player \n name:{self.name}  \n start_point:{self.start_point} \n occupied_coordinates:{self.occupied_hexagons}  \n cubes:{self.cubes}  >"

    def get_round_score(self):
        hex_types = list(map(lambda hex: hex.type, self.occupied_hexagons))
        player_score = self.score
        if "material" in hex_types:
            self.score.material = 4
            for hex in self.occupied_hexagons:
                player_score.add_score(hex)
        else:
            for hex in self.occupied_hexagons:
                player_score.add_score(hex, account_material=True)

        return player_score

    def check_skill(self, type: PlayerSkillType):
        for skill in self.skills:
            if (skill.type == type and skill.charges > 0):
                return True

        return False

    def use_skill(self, type: PlayerSkillType):
        for skill in self.skills:
            if(skill.type == type):
                skill.charges -= 1
                return