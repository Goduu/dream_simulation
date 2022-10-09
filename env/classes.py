

# HELPERS
from enum import Enum
from typing import List


class HexType(Enum):
    RED = "red"
    DOUBLE_RED = "double-red"
    GREEN = "green"
    DOUBLE_GREEN = "double-green"
    BLUE = "blue"
    DOUBLE_BLUE = "double-blue"
    MATERIAL = "material"
    START = "start"


class HexCoordinates:

    def __init__(self, q: int, r: int, s: int) -> None:
        self.q = q
        self.r = r
        self.s = s

    def __repr__(self):
        return f"<HexCoordinates q:{self.q} r:{self.r} s:{self.s}>"

    def __eq__(self, other):
        if isinstance(other, HexCoordinates):
            return self.q == other.q and \
                self.r == other.r and \
                self.s == other.s
        return NotImplemented

    def __sub__(self, other):
        return HexCoordinates(self.q - other.q, self.r - other.r,
                              self.s - other.s)

    def __add__(self, other):
        return HexCoordinates(self.q + other.q, self.r + other.r,
                              self.s + other.s)


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


class PlayerScore:
    def __init__(self, material=4) -> None:
        self.red = 0
        self.blue = 0
        self.green = 0
        self.material = material
        self.accumulator = 0

    def __repr__(self):
        return f"<Player Score \n Acc:{self.accumulator}  \n Red:{self.red}  \n Green:{self.green}  \n Blue:{self.blue}  \n Material:{self.material}  \n  >"


#######

class Hex():
    def __init__(self, id, coordinates: HexCoordinates, type: HexType) -> None:
        self.id = id
        self.coordinates = coordinates
        self.type = type
        self.player_occupation = []

    def __repr__(self):
        return f"<HEX: type:{self.type} player_occupation:{self.player_occupation} >"

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


class Player():
    def __init__(self, id: int, name: str, start_point: Hex, cubes: int, skills: List[PlayerSkill]) -> None:
        self.id = id
        self.name = name
        self.start_point = start_point
        self.occupied_hexagons: List[Hex] = [start_point]
        self.cubes = cubes
        self.material = 4
        self.score = 0
        self.skills: List[PlayerSkill] = skills

    def __repr__(self):
        return f"<Player \n name:{self.name}  \n start_point:{self.start_point} \n occupied_coordinates:{self.occupied_hexagons}  \n cubes:{self.cubes}  >"

    def add_score(self, targetHex: Hex):
        if (targetHex.type in [HexType.BLUE, HexType.GREEN, HexType.RED]):
            return 1
        if (targetHex.type in [HexType.DOUBLE_BLUE, HexType.DOUBLE_GREEN, HexType.DOUBLE_RED]):
            return 2
        return 0

    def get_turn_score(self):
        player_score = 0

        for hex in self.occupied_hexagons:
            player_score += self.add_score(hex, account_material=True)

        return player_score

    def get_round_score(self):
        hex_types = list(map(lambda hex: hex.type, self.occupied_hexagons))
        player_score = self.score
        if "material" in hex_types:
            self.material = 4
            for hex in self.occupied_hexagons:
                player_score += self.add_score(hex)
        else:
            for hex in self.occupied_hexagons:
                if (self.material > 0):
                    player_score += self.add_score(hex)
                    self.material -= 1

        return player_score

    def check_skill(self, type: PlayerSkillType):
        for skill in self.skills:
            if (skill.type == type and skill.charges > 0):
                return True

        return False


class Start(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)


class Material(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)


class Red(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 1


class Green(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 1


class Blue(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 1


class DoubleRed(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 2


class DoubleGreen(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 2


class DoubleBlue(Hex):
    def __init__(self, coordinates: HexCoordinates, type: HexType):
        super(Hex, self).__init__(coordinates, type)
        self.value = 2


class Board:

    def __init__(self, hexs: List[Hex]) -> None:
        self.hexs = hexs

    def __repr__(self):
        return f"<Board:{self.hexs} >"

    def find_hex_by_coordinates(self, coordinates: HexCoordinates):
        for h in self.hexs:
            if (h.coordinates == coordinates):
                return h

    def add_hex(self, new_hex: Hex):
        self.hexs.append(new_hex)

    def hex_exists(self, coord: HexCoordinates):
        for h in self.hexs:
            if h.coordinates == coord:
                return True
        return False
