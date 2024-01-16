import asyncio
from card_optimization.evaluate_fitness import evaluate_fitness
from card_optimization.initialize_population import initialize_population
from card_optimization.card_metrics import CardMetrics
from card_optimization.selection import selection
from card_optimization.mutate import mutate
from card_optimization.crossover import crossover
from card_optimization.check_termination_condition import check_termination_condition
from card_optimization.monte_carlo import run_monte_carlo_simulation
from card_optimization.chromosome import transform_dna_in_card

max_generations = 10


def run_genetic_algorithm():
    population, cards, metrics = initialize_population()
    num_parents = 4
    mutation_rate = 0.05
    fitness_scores_per_iteration = []

    for generation in range(max_generations):
        print("Generation:", generation)
        updated_metrics, total_games = run_monte_carlo_simulation(cards, metrics)

        fitness_scores = evaluate_fitness(cards, updated_metrics, total_games)

        if check_termination_condition(generation, max_generations, fitness_scores):
            break

        selected = selection(population, fitness_scores, num_parents)
        offspring = []

        # Perform crossover in pairs
        for i in range(0, len(selected), 2):
            off1, off2 = crossover(selected[i], selected[i + 1])
            offspring.extend([off1, off2])

        # Apply mutation to each offspring
        mutants = [mutate(dna, mutation_rate) for dna in offspring]

        # Implementing Elitism: Preserve the best individuals
        new_members = len(mutants)
        elites = population[:-new_members]

        population = elites + mutants
        cards = [transform_dna_in_card(dna) for dna in population]
        metrics = [CardMetrics(card.id) for card in cards]
        fitness_scores_per_iteration.append(sum(fitness_scores))

    return cards, fitness_scores_per_iteration, metrics
