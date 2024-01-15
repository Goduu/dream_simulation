class CardMetrics:
    def __init__(self, card_id):
        self.card_id = card_id
        self.usage_count = 0  # Total number of times the card is used
        self.win_count = 0  # Number of times the card is part of a winning strategy
        self.strategy_counts = (
            {}
        )  # Dictionary to count occurrences in different strategies

    def record_usage(self):
        """Increments the usage count of the card."""
        self.usage_count += 1

    def record_win(self):
        """Increments the win count of the card."""
        self.win_count += 1

    def record_strategy(self, strategy):
        """
        Records the usage of the card in a particular strategy.
        :param strategy: A string representing a strategy
        """
        if strategy not in self.strategy_counts:
            self.strategy_counts[strategy] = 0
        self.strategy_counts[strategy] += 1

    def calculate_usage_score(self, total_games):
        """
        Calculate the usage score of the card.
        :param total_games: Total number of games played in the simulation.
        :return: The usage score of the card.
        """
        return self.usage_count / total_games if total_games > 0 else 0

    def calculate_win_impact_score(self, total_wins):
        """
        Calculate the win impact score of the card.
        :param total_wins: Total number of wins in the simulation.
        :return: The win impact score of the card.
        """
        win_rate = self.win_count / total_wins if total_wins > 0 else 0
        # You might want to normalize this rate or apply a different formula based on your game's context
        return win_rate

    def calculate_strategy_diversity_score(self):
        """
        Calculate the strategy diversity score of the card.
        :return: The strategy diversity score of the card.
        """
        total_strategies = sum(self.strategy_counts.values())
        diversity_score = (
            len(self.strategy_counts) / total_strategies if total_strategies > 0 else 0
        )
        return diversity_score
