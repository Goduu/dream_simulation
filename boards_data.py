
from board import Board
from hex_coordinates import HexCoordinates
from player import Hex, Player, PlayerSkill, PlayerSkillType


p1_start_coord = HexCoordinates(0, -2, 2)
p2_start_coord = HexCoordinates(2, -2, 0)
p3_start_coord = HexCoordinates(-2, 2, 0)
p4_start_coord = HexCoordinates(0, 2, -2)

blue_four = Hex(0, coordinates=HexCoordinates(2, 0, -2), type="blue")
start_one = Hex(1, coordinates=p1_start_coord, type="start")
start_two = Hex(2, coordinates=p2_start_coord, type="start")
start_three = Hex(3, coordinates=p3_start_coord, type="start")
start_four = Hex(4, coordinates=p4_start_coord, type="start")

red_one = Hex(5, coordinates=HexCoordinates(-1, -1, 2), type="red")
red_two = Hex(6, coordinates=HexCoordinates(0, 0, 0), type="double-red")
red_three = Hex(7, coordinates=HexCoordinates(1, 1, -2), type="red")

blue_one = Hex(8, coordinates=HexCoordinates(2, -1, -1), type="blue")
blue_two = Hex(9, coordinates=HexCoordinates(1, 0, -1), type="double-blue")
blue_three = Hex(10, coordinates=HexCoordinates(-2, 1, 1), type="blue")

green_one = Hex(11, coordinates=HexCoordinates(1, -1, 0), type="green")
green_two = Hex(12, coordinates=HexCoordinates(-1, 0, 1), type="double-green")
green_three = Hex(13, coordinates=HexCoordinates(-1, 1, 0), type="green")

material_one = Hex(14, coordinates=HexCoordinates(0, -1, 1), type="material")
material_two = Hex(15, coordinates=HexCoordinates(0, 1, -1), type="material")


skillReset = PlayerSkill(PlayerSkillType.RESET, 1)

hexs = [
    start_one, start_two, start_three, start_four, red_one, red_two, red_three,
    blue_one, blue_two, blue_three, blue_four, green_one, green_two,
    green_three, material_one, material_two
]

p1 = Player(0, "player_0", start_point=start_one, cubes=3, skills=[skillReset])
p2 = Player(1, "player_1", start_point=start_two, cubes=3, skills=[skillReset])
p3 = Player(2, "player_2", start_point=start_three, cubes=3, skills=[skillReset])
p4 = Player(3, "player_3", start_point=start_four, cubes=3, skills=[skillReset])
players = [p1, p2, p3, p4]
board = Board()
for hex in hexs:
    board.add_hex(hex)
for player in players:
    board.add_player(player)
