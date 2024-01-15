import copy
import random

from card_optimization.chromosome import DNA


def crossover(parent1: DNA, parent2: DNA):
    """
    Performs a single-point crossover between two DNAs.

    :param parent1: The first parent DNA.
    :param parent2: The second parent DNA.
    :return: Two new offspring DNAs.
    """
    # Ensure parent DNAs are not the same object
    if parent1 is parent2:
        return parent1, parent2

    # Create deep copies to avoid modifying the original parents
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)

    # Choose a crossover point
    crossover_point = random.randint(0, 3)  # Assuming there are 4 genes

    if crossover_point == 1:
        offspring1.cost, offspring2.cost = offspring2.cost, offspring1.cost
    elif crossover_point == 2:
        offspring1.on_play_effect, offspring2.on_play_effect = (
            offspring2.on_play_effect,
            offspring1.on_play_effect,
        )
    elif crossover_point == 3:
        offspring1.passive_effect, offspring2.passive_effect = (
            offspring2.passive_effect,
            offspring1.passive_effect,
        )
    else:
        offspring1.points, offspring2.points = offspring2.points, offspring1.points

    return offspring1, offspring2
