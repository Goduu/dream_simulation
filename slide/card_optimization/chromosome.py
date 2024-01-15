import random

from classes.backpack_item import Fish, FishType
from classes.card import (
    Card,
    CardAgent,
    CardPassiveReward,
    CardPassiveTrigger,
    CardOnPlayReward,
)
from typing import List, Union
from classes.backpack_item import FishType
from classes.card import CardAgent, CardPassiveTrigger, CardOnPlayReward


class GeneType:
    def __init__(
        self, name, feature, feature_range, quantity_range, effect_agent=[], triggers=[]
    ):
        self.name = name
        self.feature = feature
        self.feature_range = feature_range
        self.quantity_range = quantity_range
        self.effect_agent = effect_agent
        self.triggers = triggers

    def __repr__(self) -> str:
        return f"GeneType: {self.name}"

    @classmethod
    def get_gene_type(cls, gene_type_name):
        for gene_type in cls:
            if gene_type.name == gene_type_name:
                return gene_type
        return None

    @property
    def features(self):
        return self.feature

    @property
    def min_feature_range(self):
        return self.feature_range[0]

    @property
    def max_feature_range(self):
        return self.feature_range[1]

    @property
    def min_quantity_range(self):
        return self.quantity_range[0]

    @property
    def max_quantity_range(self):
        return self.quantity_range[1]


CostGene = GeneType(
    "Cost",
    [fish_type for fish_type in FishType],
    [1, 3],
    [1, 3],
    [CardAgent.YOURSELF],
    [None],
)
PointsGene = GeneType("Points", [None], [1, 1], [-1, 4], [CardAgent.YOURSELF], [None])
OnPlayEffectGene = GeneType(
    "OnPlayEffect",
    [card_reward for card_reward in CardOnPlayReward],
    [0, 2],
    [-2, 2],
    [effect_agent for effect_agent in CardAgent],
    [None],
)
PassiveEffectGene = GeneType(
    "PassiveEffect",
    [card_reward for card_reward in CardPassiveReward],
    [0, 2],
    [1, 1],
    [effect_agent for effect_agent in CardAgent],
    [effect_trigger for effect_trigger in CardPassiveTrigger],
)

GeneTypes = [
    CostGene,
    OnPlayEffectGene,
    PassiveEffectGene,
    PointsGene,
]

Feature = Union[CardAgent, CardPassiveTrigger, CardOnPlayReward, FishType]


class Chromosome:
    def __init__(
        self,
        feature: Feature,
        quantity: int,
        agent: CardAgent,
        trigger: CardPassiveTrigger,
    ):
        self.feature = feature
        self.quantity = quantity
        self.agent = agent
        self.trigger = trigger


class Gene:
    def __init__(self, name: str, type: GeneType, chromosome: Chromosome):
        self.name = name
        self.type = type
        self.chromosome = chromosome

    def __repr__(self) -> str:
        return f"Gene: {self.name}, {self.chromosome.feature}: {self.chromosome.quantity}, {self.chromosome.agent}, {self.chromosome.trigger}"


class DNA:
    def __init__(
        self,
        costs: List[Gene],
        on_play_effects: List[Gene],
        passive_effects: List[Gene],
        points: List[Gene],
    ):
        self.cost = costs
        self.on_play_effect = on_play_effects
        self.passive_effect = passive_effects
        self.points = points

    def __repr__(self) -> str:
        return f"DNA: cost: {self.cost} \n on_play_effect: {self.on_play_effect} \n passive_effect: {self.passive_effect} \n points: {self.points}"


def generate_random_dna():
    dna_genes = []

    for gene_type in GeneTypes:
        feature_quantity = random.choice(
            range(gene_type.min_feature_range, gene_type.max_feature_range + 1)
        )
        for i in range(feature_quantity):
            feature = random.choice(gene_type.features)
            quantity = random.choice(
                range(gene_type.min_quantity_range, gene_type.max_quantity_range + 1)
            )
            agent = (
                random.choice(gene_type.effect_agent)
                if gene_type.effect_agent != []
                else CardAgent.YOURSELF
            )
            trigger = (
                random.choice(gene_type.triggers) if gene_type.triggers != [] else None
            )
            chromosome = Chromosome(feature, quantity, agent, trigger)
            gene = Gene(f"{gene_type.name}_{str(i)}", gene_type, chromosome)
            dna_genes.append(gene)

    cost_gene = [gene for gene in dna_genes if gene.type.name == "Cost"]
    on_play_effect_gene = [
        gene for gene in dna_genes if gene.type.name == "OnPlayEffect"
    ]
    passive_effect_gene = [
        gene for gene in dna_genes if gene.type.name == "PassiveEffect"
    ]
    points_gene = [gene for gene in dna_genes if gene.type.name == "Points"]
    dna = DNA(
        costs=cost_gene,
        on_play_effects=on_play_effect_gene,
        passive_effects=passive_effect_gene,
        points=points_gene,
    )
    return dna


# define a function that makes a short_name for a card considering the passive effect and on play effect of it
def make_description(dna: DNA) -> str:
    short_name = ""
    if dna.passive_effect:
        for gene in dna.passive_effect:
            short_name += f"When {gene.chromosome.trigger} get {gene.chromosome.quantity} {gene.chromosome.feature} "
    if dna.on_play_effect:
        for gene in dna.on_play_effect:
            short_name += (
                f"When play get {gene.chromosome.quantity} {gene.chromosome.feature} "
            )

    return short_name


def make_short_name(dna: DNA) -> str:
    short_name = ""
    if dna.passive_effect:
        for gene in dna.passive_effect:
            short_name += (
                f"{gene.chromosome.trigger.value}Get{gene.chromosome.feature.value} "
            )
    if dna.on_play_effect:
        for gene in dna.on_play_effect:
            short_name += (
                f"Get{gene.chromosome.quantity}{gene.chromosome.feature.value} "
            )

    return short_name


def transform_dna_in_card(dna: DNA) -> Card:
    cost = [
        (Fish(gene.chromosome.feature), gene.chromosome.quantity) for gene in dna.cost
    ]
    card_type = "Passive" if dna.on_play_effect == [] else "OnPlay"
    passive_effect = {
        gene.chromosome.trigger: {gene.chromosome.feature: gene.chromosome.quantity}
        for gene in dna.passive_effect
    }
    on_play_effects = {
        gene.chromosome.agent: {gene.chromosome.feature: gene.chromosome.quantity}
        for gene in dna.on_play_effect
    }
    description = make_description(dna)
    short_name = make_short_name(dna)
    points = sum([gene.chromosome.quantity for gene in dna.points])
    quantity = 1
    return Card(
        short_name=short_name,
        cost=cost,
        card_type=card_type,
        passive_effect=passive_effect,
        on_play_effects=on_play_effects,
        description=description,
        points=points,
        quantity=quantity,
    )
