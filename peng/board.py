import random
from typing import List
from functions import get_hex_coord, get_next_hex
from hex_coordinates import HexCoordinates
from penguin import Penguin
from hex import Hex, find_hex_by_coordinates
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from player import Player
import numpy as np

class Board:

    def __init__(self) -> None:
        self.hexs: List[Hex] = []
        self.players: List[Player] = []
    
    def set_players(self, players: List[Player]):
        self.players = players

    def __repr__(self):
        return f"<Board:{self.hexs} >"

    def print(self):
        for h in self.hexs:
            print(h)
            
    def find_penguin_hex_occupation(self, hex: Hex):
        for player in self.players:
            for penguin in player.penguins:
                if penguin.position == hex:
                    return penguin
    
    def find_penguins_player(self,penguin: Penguin):
        for player in self.players:
            for p in player.penguins:
                if p == penguin:
                    return player

    def add_hex(self, new_hex: Hex):
        self.hexs.append(new_hex)
    
    def add_penguin(self, new_player: Penguin):
        player_hexagon = new_player.start_point
        player_hexagon.player_occupation = new_player
        player_hexagon.occupation_number = new_player.cubes
        self.players.append(new_player)

    def hex_exists(self, coord: HexCoordinates):
        for h in self.hexs:
            if h.coordinates == coord:
                return True
        return False


    def new_round(self):
        for hex in self.hexs:
            hex.occupation_number = 0
            hex.player_occupation = None
            
    
    def get_hex_color(self,hex: Hex):
        penguin = self.find_penguin_hex_occupation(hex)
        player = self.find_penguins_player(penguin)
        return player.color if player else "white"
    
    def get_hex_penguin_type(self,hex: Hex):
        penguin = self.find_penguin_hex_occupation(hex)
        return penguin.type.value if penguin else ""
    
    def get_hex_penguin_next_hex_dir(self,hex: Hex):
        penguin = self.find_penguin_hex_occupation(hex)
        if penguin and penguin.nextHex:
            return   penguin.nextHex.coordinates - penguin.position.coordinates + penguin.position.coordinates
        return HexCoordinates(q=110,r=110,s=110)

    def mov_penguin(self, penguin: Penguin):
        movements_left = penguin.get_movement()
        if movements_left == 0:
            raise Exception("No movement left")
        
        print("coordinates,position", penguin.position)
        print("coordinates, nextHex", penguin.nextHex)
        next_hex_coord = get_next_hex(penguin.position.coordinates,penguin.nextHex.coordinates)
        next_hex = find_hex_by_coordinates(self.hexs, next_hex_coord)
        penguin.set_position( penguin.nextHex,self.hexs)
        penguin.set_next_hex(next_hex)
        penguin.set_movement(movements_left - 1)
    
    def plot_board(self, save_fig=False):
        coord = list(map(get_hex_coord, self.hexs))
        colors = list(map(self.get_hex_color, self.hexs))
        labels = list(map(self.get_hex_penguin_type, self.hexs))
        nex_hex_dir = list(map(self.get_hex_penguin_next_hex_dir, self.hexs))
        
        # Horizontal cartesian coords
        hcoord = [c.r for c in coord]
        # Vertical cartersian coords
        vcoord = [
            2. * np.sin(np.radians(60)) * (c.q - c.s) / 3. for c in coord
        ]
        # Horizontal cartesian coords
        hcoord_next = [c.r for c in nex_hex_dir]
        # Vertical cartersian coords
        vcoord_next = [
            2. * np.sin(np.radians(60)) * (c.q - c.s) / 3. for c in nex_hex_dir
        ]
        
        fig, ax = plt.subplots(1, figsize=(8, 8))
        ax.set_aspect('equal')

        for x, y, c, l, nx, ny in zip(hcoord, vcoord, colors, labels, hcoord_next, vcoord_next):
            color = c[0] 
            hex = RegularPolygon((x, y),
                                 numVertices=6,
                                 radius=2. / 3.2,
                                 orientation=np.radians(30),
                                 facecolor=color,
                                 alpha=0.7,
                                 edgecolor="red" if
                                 (color == "cyan" or color == "lime"
                                  or color == "coral") else 'k')
            ax.add_patch(hex)
            # Also add a text label
            ax.text(x, y + 0.2, l, ha='center', va='top', size=20)
            ax.text(nx+random.choice([0.02,0.01,0.03,0.04]), ny + random.choice([0.2,0.1,0.3,0.4]), "X", ha='center', va='top', size=10, color=c)
        plt.xlim([-4.5, 4])
        plt.ylim([-4.2, 4.5])
        plt.axis('off')
        if(save_fig):
            plt.savefig(
                    "./roundturn" +
                    "pname.png",
                    dpi='figure',
                    format=None,
                    metadata=None,
                    bbox_inches=None,
                    pad_inches=0.1,
                    facecolor='auto',
                    edgecolor='auto',
                )
        plt.show()
    
    
