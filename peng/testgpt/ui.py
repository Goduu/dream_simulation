from typing import Tuple
from test import FishyPenguinsGame
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import RegularPolygon
import numpy as np

def calculate_new_position(current_position: Tuple[int, int, int], direction: str, hexagons_to_move: int) -> Tuple[int, int, int]:
    # Implement logic to calculate the new position based on the chosen direction and hexagons to move
    q, r, s = current_position
    if direction == 'q':
        r -= hexagons_to_move
        s += hexagons_to_move
    elif direction == 'r':
        q += hexagons_to_move
        s -= hexagons_to_move
    elif direction == 's':
        q -= hexagons_to_move
        r += hexagons_to_move
    elif direction == 'cq':
        r += hexagons_to_move
        s -= hexagons_to_move
    elif direction == 'cr':
        q -= hexagons_to_move
        s += hexagons_to_move
    elif direction == 'cs':
        q += hexagons_to_move
        r -= hexagons_to_move
    else:
        print("Invalid direction.")
        pass
    return q, r, s

def visualize_board(game: FishyPenguinsGame):
    fig, ax = plt.subplots()

    hex_size = 0.5  # Adjust the hexagon size
    hex_spacing = 5.  # Adjust the spacing between hexagons

    # Plot hexagons
    for hexagon in game.board:
        hex_coords = np.array([hexagon.q, hexagon.r, hexagon.s])
        hex_center = hexagon_center(hex_coords, hex_size, hex_spacing)
        hex_patch = RegularPolygon(hex_center, numVertices=6, radius=hex_size, orientation=np.radians(30), edgecolor='k', facecolor='none')
        ax.add_patch(hex_patch)

        # Show fish quantity on hexagon
        ax.text(*hex_center, f'{hexagon.q},{hexagon.r},{hexagon.s}', ha='left', va='bottom', color='red')
        ax.text(*hex_center, str(hexagon.fish_quantity), ha='center', va='center', color='blue')

    # Plot penguins
    for player in game.players:
        for penguin in player.penguins:
            if penguin.position is not None:
                penguin_coords = np.array([penguin.position[0], penguin.position[1], penguin.position[2]])
                penguin_center = hexagon_center(penguin_coords, hex_size, hex_spacing)
                direction_coord = calculate_new_position(penguin_coords, penguin.direction, 1)
                direction_center = hexagon_center(direction_coord, hex_size, hex_spacing)
                # Draw arrow to represent penguin direction
                draw_arrow(ax, penguin_center, direction_center, hex_size, hex_spacing)

    # Show player information
    for i, player in enumerate(game.players):
        player_info = f"P{i + 1}"
        ax.text(0, -i, player_info, ha='left', va='center', color='black')

    ax.set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.show()

def hexagon_center(coords, hex_size, hex_spacing):
    q,r,s = coords
    x = r
    y = 2. * np.sin(np.radians(60)) * (q - s) / 3.
    return x, y

def draw_arrow(ax, center, direction_center, hex_size, hex_spacing):
    arrow_size = hex_size * 0.2  # Adjust arrow size
    arrow_length = hex_size * 0.6  # Adjust arrow length
    dx,dy = direction_center[0] - center[0], direction_center[1] - center[1]
    ax.arrow(center[0], center[1], dx,dy, head_width=arrow_size, head_length=arrow_size, fc='black', ec='black')
