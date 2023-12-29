from board import Board
from player import Player
from hex import Hex,HexType, find_hex_by_coordinates
from hex_coordinates import HexCoordinates
import random

coords = [[0,0,0],[0,1,-1],[-1,1,0],[-1,0,1],[0,-1,1],[1,-1,0],[1,0,-1],
         [1,-2,1],[2,-2,0],[2,-1,-1],[2,0,-2],[1,1,-2],[0,2,-2],[-1,2,-1],
         [-2,2,0],[-2,1,1],[-2,0,2],[-1,-1,2],[0,-2,2]]

hexcoords = HexCoordinates(q = coords[1][0], r=coords[1][1], s=coords[1][2])



border_coords = [[2,-3,1],[3,-3,0],[3,-2,-1],[3,-1,-2],[3,0,-3],
                  [2,1,-3],[1,2,-3],[0,3,-3],[-1,3,-2],[-2,3,-1],[-3,3,0],[-3,2,1],
                  [-3,1,2],[-3,0,3],[-2,-1,3],[-1,-2,3],[0,-3,3],[1,-3,2]]

# return a list with the duplicate values between two lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


board = Board()

# make a instance for 4 players
p1 = Player(0, "player_0", "red")
p2 = Player(1, "player_1", "blue")
p3 = Player(2, "player_2", "green")
p4 = Player(3, "player_3", "yellow")

board.set_players([p1, p2, p3, p4])



# For each coordinate in the list, create a hex and add it to the board
for i in range(len(coords)):
    random_type = random.choice([HexType.R1,HexType.R2,HexType.R3,HexType.R4])  # Randomly select a hex type
    hex_coordinates = HexCoordinates(q = coords[i][0], r=coords[i][1], s=coords[i][2])
    board.add_hex(Hex(i, hex_coordinates, random_type))  # Add the hex with the random type

for i in range(len(border_coords)):
    hex_coordinates = HexCoordinates(q = border_coords[i][0], r=border_coords[i][1], s=border_coords[i][2])
    board.add_hex(Hex(i, hex_coordinates, HexType.BORDER))  # Add the hex with the random type
    
    
# Create a list of available coordinates
# available_coords = border_coords.copy()
available_coords = border_coords.copy()

# For each player, set their penguins' positions to a random unique coordinate
for player in [p1, p2, p3, p4]:
    for penguin in player.penguins:
        random_index = random.randint(0, len(available_coords) - 1)
        random_coord = available_coords.pop(random_index)
        board_hex = find_hex_by_coordinates(board.hexs, HexCoordinates(q=random_coord[0], r=random_coord[1], s=random_coord[2]))
        penguin.set_position(board_hex, board.hexs)
    

# create a for loop to add all the hexes to the board
# print(board.hexs.__len__())
board.plot_board()
# movement a penguin from a player
board.mov_penguin(p1.penguins[0])
board.plot_board()

