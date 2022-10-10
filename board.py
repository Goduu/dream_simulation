from typing import List
from functions import get_hex_color, get_hex_coord, get_hex_player
from hex_coordinates import HexCoordinates
from player import Player, Hex
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np


class Board:

    def __init__(self) -> None:
        self.hexs: List[Hex] = []
        self.players: List[Player] = []
        

    def __repr__(self):
        return f"<Board:{self.hexs} >"

    def print(self):
        for h in self.hexs:
            print(h)

    def find_hex_by_coordinates(self, coordinates: HexCoordinates):
        for h in self.hexs:
            if (h.coordinates == coordinates):
                return h

    def add_hex(self, new_hex: Hex):
        self.hexs.append(new_hex)
    
    def add_player(self, new_player: Player):
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
       

    def plot_board(self, interaction, pname):
        coord = list(map(get_hex_coord, self.hexs))
        colors = list(map(get_hex_color, self.hexs))
        labels = list(map(get_hex_player, self.hexs))
        # Horizontal cartesian coords
        hcoord = [c.r for c in coord]
        # Vertical cartersian coords
        vcoord = [
            2. * np.sin(np.radians(60)) * (c.q - c.s) / 3. for c in coord
        ]
        fig, ax = plt.subplots(1, figsize=(8, 8))
        ax.set_aspect('equal')

        for x, y, c, l in zip(hcoord, vcoord, colors, labels):
            color = c[0]  # matplotlib understands lower case words for colours
            hex = RegularPolygon((x, y),
                                 numVertices=6,
                                 radius=2. / 3.,
                                 orientation=np.radians(30),
                                 facecolor=color,
                                 alpha=0.7,
                                 edgecolor="white" if
                                 (color == "cyan" or color == "lime"
                                  or color == "coral") else 'k')

            ax.add_patch(hex)
            # Also add a text label
            ax.text(x, y + 0.2, l[0], ha='center', va='top')
        plt.xlim([-3, 3])
        plt.ylim([-3, 3])
        plt.axis('off')
        # Add a table at the bottom of the axes
        plt.savefig(
            "./env/roundturn" +
            str(interaction) + "pname" + pname + ".png",
            dpi='figure',
            format=None,
            metadata=None,
            bbox_inches=None,
            pad_inches=0.1,
            facecolor='auto',
            edgecolor='auto',
        )
        # plt.show()
        plt.close()
