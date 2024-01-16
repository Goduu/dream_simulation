import json
from card_optimization.genetic_algorithm import run_genetic_algorithm
import matplotlib.pyplot as plt


# Convert objects to a JSON string and save to file
def open_cards():
    with open("objects.json", "r") as inp:  # 'r' for reading in text mode
        loaded_objects = json.load(inp)
    return loaded_objects


def plot_fitness_scores(fitness_scores_per_iteration):
    """
    Plot the sum of fitness scores per iteration using matplotlib.

    :param fitness_scores_per_iteration: A list of sum of fitness scores for each iteration.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_scores_per_iteration, marker="o", linestyle="-")
    plt.title("Sum of Fitness Scores per Iteration")
    plt.xlabel("Iteration")
    plt.ylabel("Sum of Fitness Scores")
    plt.grid(True)
    plt.show()


# Load JSON data from file and convert back to Python objects


print("comecou")
cards, fitness_scores_per_iteration, metrics = run_genetic_algorithm()

plot_fitness_scores(fitness_scores_per_iteration)

with open("cards.json", "w") as outp:  # 'w' for writing in text mode
    json.dump([card.to_json() for card in cards], outp)
