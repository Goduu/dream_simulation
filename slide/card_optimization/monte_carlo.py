from typing import List
from card_optimization.card_metrics import CardMetrics
from classes.card import Card
from game import SlideGame

num_simulations = 20

def monte_carlo_simulation(cards: List[Card], metrics: List[CardMetrics]):
    for i in range(num_simulations):
        print("Starting game...", i)
        game = SlideGame(4, cards, metrics)
        end_game = False
        while not end_game:
            end_game = game.play_turn()
            
    return game.metrics, num_simulations
