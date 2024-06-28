from hex import Hex
from hex_coordinates import HexCoordinates
from board import Board
from player import Player

# ---#S###S##
# ---R#L#G#B#
# ---#G#R#B#B
# ---B#G#L#R#
# ---#S###S##
p1_start_coord = HexCoordinates(0, -2, 2)
p2_start_coord = HexCoordinates(2, -2, 0)
p3_start_coord = HexCoordinates(-2, 2, 0)
p4_start_coord = HexCoordinates(0, 2, -2)

start_one = Hex(coordinates=p1_start_coord, type="start")
start_two = Hex(coordinates=p2_start_coord, type="start")
start_three = Hex(coordinates=p3_start_coord, type="start")
start_four = Hex(coordinates=p4_start_coord, type="start")

red_one = Hex(coordinates=HexCoordinates(-1, -1, 2), type="red")
red_two = Hex(coordinates=HexCoordinates(0, 0, 0), type="double-red")
red_three = Hex(coordinates=HexCoordinates(1, 1, -2), type="red")

blue_one = Hex(coordinates=HexCoordinates(2, -1, -1), type="blue")
blue_two = Hex(coordinates=HexCoordinates(1, 0, -1), type="double-blue")
blue_three = Hex(coordinates=HexCoordinates(-2, 1, 1), type="blue")
## should be other color
blue_four = Hex(coordinates=HexCoordinates(2, 0, -2), type="blue")

green_one = Hex(coordinates=HexCoordinates(1, -1, 0), type="green")
green_two = Hex(coordinates=HexCoordinates(-1, 0, 1), type="double-green")
green_three = Hex(coordinates=HexCoordinates(-1, 1, 0), type="green")

load_one = Hex(coordinates=HexCoordinates(0, -1, 1), type="load")
load_two = Hex(coordinates=HexCoordinates(0, 1, -1), type="load")

hexs = [
    start_one, start_two, start_three, start_four, red_one, red_two, red_three,
    blue_one, blue_two, blue_three, blue_four, green_one, green_two,
    green_three, load_one, load_two
]

board = Board()

for h in hexs:
    board.add_hex(h)

p1 = Player("p1", start_point=p1_start_coord, cubes=3, material=4)
p2 = Player("p2", start_point=p2_start_coord, cubes=3, material=4)
p3 = Player("p3", start_point=p3_start_coord, cubes=3, material=4)
p4 = Player("p4", start_point=p4_start_coord, cubes=3, material=4)

players = [p1, p2, p3, p4]

for p in players:
    board.add_player(p)
