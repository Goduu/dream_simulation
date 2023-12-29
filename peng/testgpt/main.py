# Example usage
from test import FishyPenguinsGame
from ui import visualize_board


game = FishyPenguinsGame(num_players=2)
for i in range(40):
    game.play_turn()
    
    visualize_board(game)