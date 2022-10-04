from typing import List
from functions import get_hex_color, get_hex_coord, get_hex_player, get_next_tile_coords_after_push, play_log, simple_move
from hex import Hex
from hex_coordinates import HexCoordinates
from player import Player
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

    def plot_board(self, interaction, pname):
        coord = list(map(get_hex_coord, self.hexs))
        colors = list(map(get_hex_color, self.hexs))
        labels = list(map(get_hex_player, self.hexs))
        # Horizontal cartesian coords
        hcoord = [c.q for c in coord]

        # Vertical cartersian coords
        vcoord = [
            2. * np.sin(np.radians(60)) * (c.s - c.r) / 3. for c in coord
        ]
        fig, ax = plt.subplots(1)
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
        plt.xlim([-4, 4])
        plt.ylim([-4, 4])
        plt.savefig(
            "./figs/" + str(interaction) + pname + ".png",
            dpi='figure',
            format=None,
            metadata=None,
            bbox_inches=None,
            pad_inches=0.1,
            facecolor='auto',
            edgecolor='auto',
        )
        plt.show()

    def find_hex_by_coordinates(self, coordinates: HexCoordinates):
        for h in self.hexs:
            if (h.coordinates == coordinates):
                return h

    def find_player_by_coordinates(self, coordinates: HexCoordinates):
        for player in self.players:
            for player_coordinates in player.occupied_coordinates:
                if (player_coordinates == coordinates):
                    return player

    def add_hex(self, new_hex: Hex):
        self.hexs.append(new_hex)

    def add_player(self, new_player: Player):
        self.players.append(new_player)
        player_hexagon = self.find_hex_by_coordinates(new_player.start_point)
        for i in range(new_player.cubes):
            player_hexagon.player_occupation.append(new_player)

    def hex_exists(self, coord: HexCoordinates):
        for h in self.hexs:
            if h.coordinates == coord:
                return True
        return False

    def can_push(self, coord: HexCoordinates, coord_target: HexCoordinates):
        coord_to_move_pushed_player = get_next_tile_coords_after_push(
            coord, coord_target)
        hex_to_move_pushed_player = self.find_hex_by_coordinates(
            coord_to_move_pushed_player)

        if (hex_to_move_pushed_player
                and hex_to_move_pushed_player.player_occupation == []):
            return True
        return False

    def is_movement_possible(self, coord: HexCoordinates,
                             coord_target: HexCoordinates):
        if self.hex_exists(coord_target):
            hexagon_target = self.find_hex_by_coordinates(coord_target)
            if hexagon_target.type == "start":
                return False
            elif len(hexagon_target.player_occupation) == 0:
                return True
            elif self.can_push(coord, coord_target):
                return True

    def check_movement_possibilities(self, player: Player):
        mov_possibilities = []
        for occupied_coord in player.occupied_coordinates:
            hex = self.find_hex_by_coordinates(occupied_coord)
            surrounding_coordinates = hex.get_surroundings()
            for sur_coord in surrounding_coordinates:
                if (self.is_movement_possible(hex.coordinates, sur_coord)):

                    mov_possibilities.append({
                        "from_coord": occupied_coord,
                        "target_coord": sur_coord
                    })

        return mov_possibilities

    #can just be move if movement is possible
    def mov_player(self, from_coord: HexCoordinates,
                   target_coord: HexCoordinates, start_coord: HexCoordinates):
        from_player = self.find_player_by_coordinates(from_coord)
        start_hexagon = self.find_hex_by_coordinates(start_coord)
        from_hexagon = self.find_hex_by_coordinates(from_coord)
        target_hexagon = self.find_hex_by_coordinates(target_coord)
        target_player = len(target_hexagon.player_occupation
                            ) > 0 and target_hexagon.player_occupation[0]

        # push movement
        if (target_player and isinstance(target_player, Player)):
            next_hex_coords = get_next_tile_coords_after_push(
                from_coord, target_coord)
            next_hexagon = self.find_hex_by_coordinates(next_hex_coords)
            play_log("push", from_player, target_hexagon, next_hexagon,
                     target_player)
            simple_move(target_hexagon, next_hexagon)
            target_player.occupied_coordinates.remove(target_coord)
            target_player.occupied_coordinates.append(next_hex_coords)
            #if pushed target is startpoint gives pushed player 1 cube
            if (next_hexagon.type == "start"):
                target_player.cubes += 1

        play_log("move", from_player, from_hexagon, target_hexagon)
        simple_move(start_hexagon, target_hexagon)

        from_player.cubes -= 1
        from_player.occupied_coordinates.append(target_coord)

        #if start point occupation == 0 remove it form hexagons occupation
        if (from_hexagon.type == "start"
                and len(from_hexagon.player_occupation) == 0):
            from_player.occupied_coordinates.remove(from_hexagon.coordinates)

        return
