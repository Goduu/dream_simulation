# Adapted from https://mblogscode.com/2016/06/03/python-naughts-crossestic-tac-toe-coding-unbeatable-ai/

from ast import List
from all_cards import get_all_cards
from dream_simulation.slide.classes.backpack_item import BackpackItem, FishType, Ice
from dream_simulation.slide.classes.card import Card
from dream_simulation.slide.constants import Dir
from dream_simulation.slide.get_possible_actions import get_possible_actions
from game import SlideGame
from possible_actions_mapping import (
    get_action_index_by_action,
    get_possible_actions_mapping,
)
import gym
import numpy as np

import config

from stable_baselines import logger


class Player:
    def __init__(self, id, token):
        self.id = id
        self.token = token


class Token:
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol


class SlideEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        self.possible_actions_mapping = get_possible_actions_mapping()
        super(SlideEnv, self).__init__()
        self.n_players = 4
        self.game = SlideGame(self.n_players)
        self.name = "slide"
        self.current_player_num = 0
        self.penguin_per_player = 3
        self.all_cards = get_all_cards()
        self.max_actions = 5
        self.action_space = gym.spaces.MultiDiscrete(
            [len(self.possible_actions_mapping)]
            * self.max_actions
            * self.penguin_per_player
        )
        self.observation_space = gym.spaces.Dict(
            {
                "players": gym.spaces.Dict(
                    {
                        player_id: gym.spaces.Dict(
                            {
                                "cards": gym.spaces.MultiBinary(
                                    self.all_cards.__len__()
                                ),
                                "terminated": gym.spaces.Discrete(2),
                                "season": gym.spaces.Discrete(3),
                                "penguins": gym.spaces.Dict(
                                    {
                                        "penguins": gym.spaces.Dict(
                                            {
                                                penguin_id: gym.spaces.Dict(
                                                    {
                                                        "movement_tokens": gym.spaces.Box(
                                                            low=0,
                                                            high=10,
                                                            shape=(1,),
                                                            dtype=np.int,
                                                        ),
                                                        "fishing_tokens": gym.spaces.Box(
                                                            low=0,
                                                            high=10,
                                                            shape=(1,),
                                                            dtype=np.int,
                                                        ),
                                                        "direction": gym.spaces.Discrete(
                                                            6
                                                        ),
                                                        "position": gym.spaces.Box(
                                                            low=-3,
                                                            high=3,
                                                            shape=(3,),
                                                            dtype=np.float32,
                                                        ),
                                                        "ice_tokens": gym.spaces.Discrete(
                                                            10
                                                        ),
                                                        "cards": gym.spaces.MultiBinary(
                                                            self.all_cards.__len__()
                                                        ),
                                                        "terminated": gym.spaces.Discrete(
                                                            2
                                                        ),
                                                        "backpack": gym.spaces.Dict(
                                                            {
                                                                "ice": gym.spaces.Discrete(
                                                                    10
                                                                ),
                                                                "fish": gym.spaces.MultiDiscrete(
                                                                    [3, 10]
                                                                ),
                                                            }
                                                        ),
                                                    }
                                                )
                                                for penguin_id in range(3)
                                            }
                                        )
                                    }
                                ),
                            }
                        )
                        for player_id in range(self.n_players)
                    }
                )
            }
        )

    def get_card_encoding(self, player_cards: List[Card]):
        card_encoding = [1 if card in player_cards else 0 for card in self.all_cards]
        return card_encoding

    def get_penguin_direction_encoding(self, penguin_direction: Dir):
        direction_encoding = [
            1 if direction == penguin_direction else 0 for direction in Dir
        ]
        return direction_encoding

    def get_penguin_backpack_encoding(self, penguin_backpack: List[BackpackItem]):
        backpack_encoding = {
            "ice": [1 if item == Ice() else 0 for item in penguin_backpack],
            "fish": [
                1
                if item.type == FishType.A
                else 2
                if item.type == FishType.B
                else 3
                if item.type == FishType.C
                else 0
                for item in penguin_backpack
            ],
        }
        return backpack_encoding

    @property
    def observation(self):
        obs = {}
        for player in self.game.players:
            obs["players"][player.id] = {
                player.id: {
                    "cards": self.get_card_encoding(player.cards),
                    "terminated": int(player.terminated),
                    "season": int(player.season),
                    "penguins": {
                        "penguins": {
                            penguin.id: {
                                "movement_tokens": penguin.movement_tokens,
                                "fishing_tokens": penguin.movement_tokens,
                                "direction": self.get_penguin_direction_encoding(
                                    penguin.direction
                                ),
                                "position": penguin.position,
                                "cards": self.get_card_encoding(penguin.cards),
                                "terminated": int(penguin.terminated),
                                "backpack": self.get_penguin_backpack_encoding(
                                    penguin.backpack
                                ),
                            }
                            for penguin in player.penguins
                        }
                    },
                }
            }

        return obs

    @property
    def legal_actions(self):
        """
        Returns a vector of legal actions for the current player
        [0 or 1] for each action in action_space (0 if illegal, 1 if legal)
        An array for each penguin -> check that @TODO
        """
        current_player = self.game.players[self.current_player_num]

        legal_actions_vector = [
            np.zeros(self.action_space.shape, dtype=bool)
            for _ in range(self.penguin_per_player)
        ]

        for penguin in current_player.penguins:
            legal_actions = get_possible_actions(
                current_player,
                penguin,
                self.game.board,
                self.game.card_market,
                self.players,
            )
            for action in legal_actions:
                legal_actions_vector[penguin.id][
                    get_action_index_by_action(action)
                ] = True

        return legal_actions_vector

    @property
    def current_player(self):
        return self.players[self.current_player_num]

    def calculate_reward(self):
        current_player = self.game.players[self.current_player_num]
        # sum all of the card.points in player.cards and in player.penguin.cards
        player_cards_points = sum([card.points for card in current_player.cards])
        player_penguin_cards_points = sum(
            [
                card.points
                for penguin in current_player.penguins
                for card in penguin.cards
            ]
        )

        return player_cards_points + player_penguin_cards_points

    def step(self, action):
        self.game.take_action(action)

        # Get the updated observation
        observation = self.observation

        # Calculate the reward for the current step
        reward = self.calculate_reward()

        # Check if the episode is done
        done = self.game.all_players_terminated()

        # Additional information (optional)
        # info = {"key": "value"}
        info = {}

        return observation, reward, done, info

        # # check move legality
        # board = self.board

        # if board[action].number != 0:  # not empty
        #     done = True
        #     reward = [1, 1]
        #     reward[self.current_player_num] = -1
        # else:
        #     board[action] = self.current_player.token
        #     self.turns_taken += 1
        #     r, done = self.check_game_over()
        #     reward = [-r, -r]
        #     reward[self.current_player_num] = r

        # self.done = done

        # if not done:
        #     self.current_player_num = (self.current_player_num + 1) % 2

        # return self.observation, reward, done, {}

    def reset(self):
        self.game = SlideGame(self.n_players)
        self.players = [Player("1", Token("X", 1)), Player("2", Token("O", -1))]
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f"\n\n---- NEW GAME ----")
        return self.observation

    def render(self, mode="human", close=False, verbose=True):
        for player in self.game.players:
            player.print_penguins()

    def rules_move(self):
        if self.current_player.token.number == 1:
            b = [x.number for x in self.board]
        else:
            b = [-x.number for x in self.board]

        # Check computer win moves
        for i in range(0, self.num_squares):
            if b[i] == 0 and testWinMove(b, 1, i):
                logger.debug("Winning move")
                return self.create_action_probs(i)
        # Check player win moves
        for i in range(0, self.num_squares):
            if b[i] == 0 and testWinMove(b, -1, i):
                logger.debug("Block move")
                return self.create_action_probs(i)
        # Check computer fork opportunities
        for i in range(0, self.num_squares):
            if b[i] == 0 and testForkMove(b, 1, i):
                logger.debug("Create Fork")
                return self.create_action_probs(i)
        # Check player fork opportunities, incl. two forks
        playerForks = 0
        for i in range(0, self.num_squares):
            if b[i] == 0 and testForkMove(b, -1, i):
                playerForks += 1
                tempMove = i
        if playerForks == 1:
            logger.debug("Block One Fork")
            return self.create_action_probs(tempMove)
        elif playerForks == 2:
            for j in [1, 3, 5, 7]:
                if b[j] == 0:
                    logger.debug("Block 2 Forks")
                    return self.create_action_probs(j)
        # Play center
        if b[4] == 0:
            logger.debug("Play Centre")
            return self.create_action_probs(4)
        # Play a corner
        for i in [0, 2, 6, 8]:
            if b[i] == 0:
                logger.debug("Play Corner")
                return self.create_action_probs(i)
        # Play a side
        for i in [1, 3, 5, 7]:
            if b[i] == 0:
                logger.debug("Play Side")
                return self.create_action_probs(i)
