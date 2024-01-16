import random
import copy

from card_optimization.chromosome import DNA


def mutate(dna: DNA, mutation_rate):
    """
    Performs mutation on a DNA object.

    :param dna: The DNA object to be mutated.
    :param mutation_rate: The probability of a gene being mutated.
    :return: Mutated DNA.
    """
    # Deep copy to avoid modifying the original DNA
    mutated_dna: DNA = copy.deepcopy(dna)
    # Mutate each gene with a probability of mutation_rate
    for genes in (
        mutated_dna.cost,
        mutated_dna.on_play_effect,
        mutated_dna.passive_effect,
        mutated_dna.points,
    ):
        if random.random() < mutation_rate:
            # Perform mutation based on the type of gene
            # print('paha eita', gene)
            if len(genes) > 0:
                if genes[0].type.name == "Cost":
                    # Example: mutate the cost
                    for gene in genes:
                        gene.chromosome.quantity = random.choice(
                            range(
                                gene.type.min_quantity_range,
                                gene.type.max_quantity_range + 1,
                            )
                        )
                elif genes[0].type.name in ["OnPlayEffect", "PassiveEffect"]:
                    # Example: mutate the effect or its quantity
                    for gene in genes:
                        gene.chromosome.feature = random.choice(gene.type.features)
                        gene.chromosome.quantity = random.choice(
                            range(
                                gene.type.min_quantity_range,
                                gene.type.max_quantity_range + 1,
                            )
                        )
                elif genes[0].type.name == "Points":
                    # Example: mutate the points
                    for gene in genes:
                        gene.chromosome.quantity = random.choice(
                            range(
                                gene.type.min_quantity_range,
                                gene.type.max_quantity_range + 1,
                            )
                        )

    return mutated_dna
