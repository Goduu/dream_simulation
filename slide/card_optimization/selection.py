import random


def selection(dnas, fitness_scores, num_parents):
    """
    Selects a number of parents for the next generation using roulette wheel selection.

    :param dnas: List of DNA objects (the current population).
    :param fitness_scores: List of fitness scores corresponding to each DNA.
    :param num_parents: Number of parents to select.
    :return: List of selected parent DNAs.
    """
    selected_parents = []
    total_fitness = sum(fitness_scores)
    normalized_fitness_scores = [score / total_fitness for score in fitness_scores]

    for _ in range(num_parents):
        cumulative_sum = 0
        random_pick = random.random()
        for dna, normalized_score in zip(dnas, normalized_fitness_scores):
            cumulative_sum += normalized_score
            if cumulative_sum > random_pick:
                selected_parents.append(dna)
                break

    return selected_parents
