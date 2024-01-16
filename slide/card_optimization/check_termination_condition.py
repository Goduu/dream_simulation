target_fitness = 100


def check_termination_condition(
    current_generation: int, max_generations: int, fitness_scores
):
    """
    Checks if the termination condition of the genetic algorithm has been met.

    :param current_generation: The current generation number.
    :param max_generations: The maximum number of generations allowed.
    :param fitness_scores: List of fitness scores corresponding to each DNA.
    :return: Boolean indicating whether the termination condition is met.
    """
    # Check if the current generation has reached the maximum limit
    if current_generation >= max_generations:
        print(
            f"Termination condition met: Reached maximum generations ({max_generations})."
        )
        return True

    # Check if the best fitness score has reached or exceeded the target
    # if sum(fitness_scores)/len(fitness_scores) >= target_fitness:
    #     print(f"Termination condition met: Target fitness level achieved (Fitness: {target_fitness}).")
    #     return True

    # If none of the conditions are met, continue the algorithm
    return False
