

from typing import List
from player import Player
import matplotlib.pyplot as plt
import numpy as np

IMG_URL = "./images/"

class ScoreAnalysis:
    def __init__(self) -> None:
        self.red = []
        self.green = []
        self.blue = []
        self.reward = []
        self.accumulator = []


class PlayerAnalysis:
    def __init__(self) -> None:
        self.player_0 = []
        self.player_1 = []
        self.player_2 = []
        self.player_3 = []


class DataCollector:
    def __init__(self) -> None:
        self.resource_analysis = ScoreAnalysis()
        self.player_analysis = PlayerAnalysis()

    def collect(self, players: List[Player]):
        for player in players:
            score = self.resource_analysis
            score.red.append(player.score.red)
            score.green.append(player.score.green)
            score.blue.append(player.score.blue)
            score.reward.append(player.score.reward)
            score.accumulator.append(player.score.accumulator)

            getattr(self.player_analysis, player.name).append(
                player.score.reward)

    def plot_resource_analysis(self):
        score = self.resource_analysis

        n_bins = 10

        fig, axs = plt.subplots(1, 5, sharey=True, tight_layout=True)
        axs[0].hist(score.red, bins=n_bins, label="Red", color="firebrick")
        axs[1].hist(score.green, bins=n_bins, label="Green", color="green")
        axs[2].hist(score.blue, bins=n_bins, label="Blue", color="mediumblue")
        axs[3].hist(score.reward, bins=n_bins, label="Reward", color="gold")
        axs[4].hist(score.accumulator, bins=n_bins,
                    label="Accumulator", color="purple")

        axs[0].set_title("Red")
        axs[1].set_title("Green")
        axs[2].set_title("Blue")
        axs[3].set_title("Reward")
        axs[4].set_title("Acc")
        plt.savefig(
            IMG_URL +"/resource_analysis" +
            str(len(score.red)) + ".png",
            dpi='figure',
            format=None,
            metadata=None,
            bbox_inches=None,
            pad_inches=0.1,
            facecolor='auto',
            edgecolor='auto',
        )
        plt.show()

    def plot_player_analysis(self):
        score = self.player_analysis

        n_bins = 10

        plotp0 = plt.subplot2grid((2, 4), (0, 0), colspan=1)
        plotp1 = plt.subplot2grid((2, 4), (0, 1), colspan=1)
        plotp2 = plt.subplot2grid((2, 4), (0, 2), colspan=1)
        plotp3 = plt.subplot2grid((2, 4), (0, 3), colspan=1)
        plotAvg = plt.subplot2grid((2, 4), (1, 0), colspan=4)
        plotp0.hist(score.player_0, bins=n_bins,
                    label="Red", color="firebrick")
        plotp1.hist(score.player_1, bins=n_bins,
                    label="Green", color="green")
        plotp2.hist(score.player_2, bins=n_bins,
                    label="Blue", color="mediumblue")
        plotp3.hist(score.player_3, bins=n_bins,
                    label="Reward", color="gold")
        means = [np.average(score.player_0), np.average(
            score.player_1), np.average(score.player_2), np.average(score.player_3)]
        plotAvg.barh([0, 1, 2, 3], means)

        plotp0.set_title("Player 0")
        plotp1.set_title("Player 1")
        plotp2.set_title("Player 2")
        plotp3.set_title("Player 3")

        plotp0.set_ylabel('Resource Distribution')

        plotAvg.set_title("Players Avg Reward")
        plotAvg.set_xlabel('Avg Reward')
        plotAvg.invert_yaxis()
        plotAvg.set_yticks(np.arange(4), labels=["p0", "p1", "p2", "p3"])

        for i, v in enumerate(means):
            plotAvg.text(v - 0.30, i +.1, str(v),
                         color='w', fontweight='bold')

        plt.tight_layout()
        plt.savefig(
            IMG_URL + "/player_analysis" +
            str(len(score.player_0)) + ".png",
            dpi='figure',
            format=None,
            metadata=None,
            bbox_inches=None,
            pad_inches=0.1,
            facecolor='auto',
            edgecolor='auto',
        )
        plt.show()
