# Example usage
from printc import MColors, printc
from game import FishyPenguinsGame
from ui import visualize_board

game = FishyPenguinsGame(num_players=4)
for i in range(400):
    end_game = game.play_turn()
    if end_game:
        break


printc("\U0001F41F", MColors.OKGREEN)
for player in game.players:
    player.print_penguins()
visualize_board(game)
