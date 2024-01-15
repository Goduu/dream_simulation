from card_optimization.card_metrics import CardMetrics
from card_optimization.chromosome import (
    generate_random_dna,
    transform_dna_in_card,
)

population_size = 25

def initialize_population():
    population = []
    cards = []
    metrics = []
    for _ in range(population_size):
        dna = generate_random_dna()
        population.append(dna)
        card = transform_dna_in_card(dna)
        cards.append(card)
        cardMetrics = CardMetrics(card.id)
        metrics.append(cardMetrics)
        
    print("paha eita")
    print(f'population-- 1{population[0]}')
    return population, cards, metrics
