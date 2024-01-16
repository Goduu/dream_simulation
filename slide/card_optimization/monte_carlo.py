import threading
import time
from typing import List
from card_optimization.card_metrics import CardMetrics
from classes.card import Card
from game import SlideGame
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import asyncio


def your_function(arg):
    # Your function logic here
    pass


# For I/O-bound tasks


num_simulations = 480


def play_game(cards: List[Card], metrics: List[CardMetrics], game_number):
    # print("Starting game...", game_number)
    game = SlideGame(4, cards, metrics)
    end_game = False
    while not end_game:
        end_game = game.play_turn()

    return game.metrics


def run_monte_carlo_simulation(cards: List[Card], metrics: List[CardMetrics]):
    for i in range(num_simulations):
        play_game(cards, metrics, i)

    return metrics, num_simulations
