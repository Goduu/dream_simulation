from typing import List

import numpy as np
from card_optimization.card_metrics import CardMetrics
from classes.card import Card, CardAgent, CardOnPlayReward
from collections import Counter


def calculate_card_quality_score(card: Card) -> int:
    # Base score from card points
    max_points_score = 4
    max_on_play_score = 8
    max_passive_score = 4
    points_score = card.points

    important_rewards = [
        CardOnPlayReward.FISHING,
        CardOnPlayReward.MOVEMENT,
        CardOnPlayReward.BACKPACK,
    ]
    # Score for active effects
    on_play_effect_score = 0
    for agent, effects in card.on_play_effect.items():
        if agent == CardAgent.YOURSELF:
            for effect, quantity in effects.items():
                # Adjust the score based on effect type and quantity
                # Assume positive effects add to the score, negative effects subtract
                effect_multiplier = 2 if effect in important_rewards else 1
                on_play_effect_score += effect_multiplier * quantity
        elif agent == CardAgent.OTHERS:
            for effect, quantity in effects.items():
                effect_multiplier = -2 if effect in important_rewards else 0.5
                on_play_effect_score += effect_multiplier * quantity
        else:
            for effect, quantity in effects.items():
                effect_multiplier = 0.5 if effect in important_rewards else 1
                on_play_effect_score += effect_multiplier * quantity

    # Score for passive effects
    passive_effect_score = 0
    for agent, effects in card.passive_effect.items():
        if agent == CardAgent.YOURSELF:
            for effect, quantity in effects.items():
                # Adjust the score based on effect type and quantity
                # Assume positive effects add to the score, negative effects subtract
                effect_multiplier = 2 if effect in important_rewards else 1
                passive_effect_score += effect_multiplier * quantity
        elif agent == CardAgent.OTHERS:
            for effect, quantity in effects.items():
                effect_multiplier = -2 if effect in important_rewards else -0.5
                passive_effect_score += effect_multiplier * quantity
        elif agent == CardAgent.ALL:
            for effect, quantity in effects.items():
                effect_multiplier = 0.5 if effect in important_rewards else 1
                passive_effect_score += effect_multiplier * quantity

    effect_score = 0
    if card.on_play_effect == {} and card.passive_effect == {}:
        effect_score = -0.25
    else:
        effect_score = 0.25

    # Combine scores to calculate total quality score
    total_score = (
        points_score / max_points_score
        + on_play_effect_score / max_on_play_score
        + passive_effect_score / max_passive_score
        + effect_score
    )
    return total_score / 4


def calculate_card_scores(
    card: Card, card_metrics: List[CardMetrics], total_games: int
):
    quality_score = calculate_card_quality_score(card)

    metric = next(
        (metrics for metrics in (card_metrics) if metrics.card_id == card.id),
        None,
    )
    usage_score = metric.calculate_usage_score(total_games)
    win_impact_score = metric.calculate_win_impact_score(total_games)
    print(f"usage_score: {usage_score}")
    print(f"win_impact_score: {win_impact_score}")
    print(f"quality_score: {quality_score}")
    return usage_score, win_impact_score, quality_score


def calculate_scores(
    card_set: List[Card], card_metrics: List[CardMetrics], total_games: int
):
    usage_scores = []
    win_impact_scores = []
    quality_scores = []
    for card in card_set:
        (
            card_usage_score,
            card_win_impact_score,
            card_quality_score,
        ) = calculate_card_scores(card, card_metrics, total_games)
        usage_scores.append(card_usage_score)
        win_impact_scores.append(card_win_impact_score)
        quality_scores.append(card_quality_score)

    # total_resources = sum(resource_usage.values())
    # resource_balance_score = {
    #     fish_type: count / total_resources
    #     for fish_type, count in resource_usage.items()
    # }
    return (usage_scores, win_impact_scores, quality_scores)


def evaluate_fitness(
    card_set: List[Card], card_metrics: List[CardMetrics], total_games: int
):
    (usage_scores, win_impact_scores, quality_scores) = calculate_scores(
        card_set, card_metrics, total_games
    )

    # Combine these scores into a final fitness score
    # The weights (w1, w2, w3, w4) can be adjusted based on what you deem more important
    w1, w2, w3 = 0.33, 0.33, 0.33  # weights
    fitness_scores = (
        w1 * np.array([usage_score for usage_score in usage_scores])
        + w2 * np.array([win_impact_score for win_impact_score in win_impact_scores])
        + w3 * np.array([quality_score for quality_score in quality_scores])
    )

    return fitness_scores
