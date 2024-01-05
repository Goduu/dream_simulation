from utils import calculate_new_position, printc
from game import SlideGame
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
import numpy as np


def visualize_board(game: SlideGame):
    fig, ax = plt.subplots()

    hex_size = 0.5  # Adjust the hexagon size
    hex_spacing = 5.0  # Adjust the spacing between hexagons

    # Plot hexagons
    for hexagon in game.board:
        hex_coords = np.array([hexagon.q, hexagon.r, hexagon.s])
        hex_center = hexagon_center(hex_coords)
        hex_patch = RegularPolygon(
            hex_center,
            numVertices=6,
            radius=hex_size,
            orientation=np.radians(30),
            edgecolor="k",
            facecolor="none",
        )
        ax.add_patch(hex_patch)

        # Show fish quantity on hexagon
        ax.text(
            *hex_center,
            f"{hexagon.q},{hexagon.r},{hexagon.s}",
            ha="left",
            va="bottom",
            color="red",
        )
        ax.text(
            *hex_center,
            str(hexagon.fish_quantity),
            ha="center",
            va="center",
            color="blue",
        )

    # Plot penguins
    for player in game.players:
        for penguin in player.penguins:
            if penguin.position is not None:
                penguin_coords = np.array(
                    [penguin.position[0], penguin.position[1], penguin.position[2]]
                )
                penguin_center = hexagon_center(penguin_coords)
                if penguin.direction is not None:
                    direction_coord = calculate_new_position(
                        penguin_coords, penguin.direction, 1
                    )
                    direction_center = hexagon_center(direction_coord)
                    # Draw arrow to represent penguin direction
                    draw_arrow(ax, penguin_center, direction_center, hex_size)

    # Show player information
    for i, player in enumerate(game.players):
        player_info = f"P{i + 1}"
        ax.text(0, -i, player_info, ha="left", va="center", color="black")

    ax.set_aspect("equal", adjustable="box")
    plt.axis("off")
    plt.autoscale(enable=True, axis="both", tight=True)
    plt.show()


def hexagon_center(coords):
    q, r, s = coords
    x = r
    y = 2.0 * np.sin(np.radians(60)) * (q - s) / 3.0
    return x, y


def draw_arrow(ax, center, direction_center, hex_size):
    arrow_size = hex_size * 0.2  # Adjust arrow size
    dx, dy = direction_center[0] - center[0], direction_center[1] - center[1]
    ax.arrow(
        center[0],
        center[1],
        dx,
        dy,
        head_width=arrow_size,
        head_length=arrow_size,
        fc="black",
        ec="black",
    )
