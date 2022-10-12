from enum import Enum
from typing import List

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

    def __init__(self, id, coordinates: HexCoordinates, type: HexType) -> None:
        self.id = id
        self.coordinates = coordinates
        self.type = type
        self.player_occupation: Player = None
        self.occupation_number = 0

    def __repr__(self):
        return f"<Hex \n type:{self.type}  \n player_occupation:{self.player_occupation and self.player_occupation.name } \n coordinates:{self.coordinates} >"

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


class PlayerScore:
    def __init__(self, red=0,  green=0, blue=0, material=4) -> None:
        self.red = red
        self.blue = blue
        self.green = green
        self.material = material
        self.accumulator = 0
        self.reward = 0

    def __repr__(self):
        return f"<Player Score \n Acc:{self.accumulator}  \n Red:{self.red}  \n Green:{self.green}  \n Blue:{self.blue}  \n Material:{self.material} \n Rewards:{self.reward}  \n  >"

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

    def get_score_list_rgb(self):
        return (self.red, self.green, self.blue, self.material)


class PlayerSkillType(Enum):
    PUSH_ROW = "push"               # Push two in a row and stay in the first hex
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

    def __init__(self, id: int, name: str, start_point: Hex, cubes: int, skills: List[PlayerSkill]) -> None:
        self.id = id
        self.name = name
        self.terminated = False
        self.start_point = start_point
        self.occupied_hexagons: List[Hex] = [start_point]
        self.cubes = cubes
        self.partialScore = PlayerScore()
        self.score = PlayerScore()
        self.skills = skills

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

    def new_round(self):
        self.cubes = 3
        for skill in self.skills:
            skill.charges += 1
        self.occupied_hexagons = [self.start_point]
        self.start_point.player_occupation = self
        self.start_point.occupation_number = self.cubes

    def check_skill(self, type: PlayerSkillType):
        for skill in self.skills:
            if (skill.type == type and skill.charges > 0):
                return True

        return False

    def use_skill(self, type: PlayerSkillType):
        for skill in self.skills:
            if (skill.type == type):
                skill.charges -= 1
                return

    def check_termination(self, mov_possibilities, buy_possibilities):
        self.terminated = (self.cubes == 0 or len(
            mov_possibilities) == 0) and len(buy_possibilities) == 0
