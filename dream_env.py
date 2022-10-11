

import copy
from random import random
from typing import List
from board import Board
from hex_coordinates import HexCoordinates
from movement_functions import MovPossibility, check_movement_possibilities, mov_player
from player import Player, Hex
import numpy as np
from boards_data import board
from rewards import RewardStore, rewards


class Observation:

    def __init__(self, observation, action_mask) -> None:
        self.observation = observation
        self.action_mask = action_mask

# TODO Add buy possibilites in Obeservation


class DreamEnv:

    def __init__(self) -> None:
        self.round = 0
        self.rounds = 3

    def pass_current_player(self):
        players_names = [player.name for player in self.board.players]
        for i in range(len(self.board.players)):
            next_player_index = players_names.index(
                self.current_player.name) + 1
            self.current_player = self.board.players[next_player_index % len(
                self.board.players)]
            if (not self.current_player.terminated):
                return

    def observe(self):

        mov_possibilities = check_movement_possibilities(
            self.board, self.current_player)

        buy_possibilities = self.reward_store.get_possible_buys(
            self.current_player)

        hex_number = len(self.board.hexs)
        rewards_number = len(self.reward_store.rewards)

        action_mask = np.zeros(hex_number + rewards_number, "int8")

        if (self.current_player.cubes > 0):
            for mov in mov_possibilities:
                target_hex = mov.target_hex
                action_mask[target_hex.id] = 1

        for buy in buy_possibilities:
            action_mask[hex_number + buy.id] = 1

        obs_array = np.zeros([len(self.board.hexs), 2], "int8")
        for player in self.board.players:
            for occupied in player.occupied_hexagons:
                if (player.id == self.current_player.id):
                    obs_array[occupied.id][0] = 1
                else:
                    obs_array[occupied.id][1] = 1

        observation = np.stack(
            obs_array, axis=1).astype(np.int8)
        return Observation(observation, action_mask)

    def get_movement_by_action(self, action, mov_possibilities: List[MovPossibility]):
        target_hex = None
        from_hex = None
        for possibility in mov_possibilities:
            if (possibility.target_hex.id == action):
                target_hex = possibility.target_hex
                from_hex = possibility.from_hex

        return target_hex, from_hex

    def get_reward_by_action(self, action):
        reward_id = action - len(self.board.hexs)
        for reward in self.reward_store.rewards:
            if reward.id == reward_id:
                return reward

    def next_round(self):
        self.round += 1
        players_copy = copy.deepcopy(self.board.players)
        self.initialize_game()
        for player_copy in players_copy:
            for player in self.board.players:
                if (player_copy.id == player.id):
                    player.score = player_copy.score
                    player.score.material = 4

    def account_resources(self):
        for player in self.board.players:
            player.get_round_score()

    def is_end_round(self):
        the_end = True
        for player in self.board.players:
            the_end = the_end and player.terminated
        return the_end

    def get_action_type(self, action: int):
        if (action >= len(self.board.hexs)):
            return "buy"
        return "mov"

    def step(self, action):
        mov_possibilities = check_movement_possibilities(
            self.board, self.current_player)
        buy_possibilities = self.reward_store.get_possible_buys(
            self.current_player)

        self.current_player.check_termination(
            mov_possibilities, buy_possibilities)

        if (not self.current_player.terminated):
            action_type = self.get_action_type(action)
            if (action_type == "mov"):
                target_hex, from_hex = self.get_movement_by_action(
                    action, mov_possibilities)
                if (target_hex):
                    mov_player(self.board, from_hex,
                               target_hex, self.current_player.start_point)
            else:
                reward_to_buy = self.get_reward_by_action(action)
                self.reward_store.buy_reward(
                    self.current_player, reward_to_buy)

        end_round = self.is_end_round()
        if (end_round):
            self.account_resources()
            if (self.round < self.rounds):
                self.next_round()
            else:
                return self.observe(), True
        self.pass_current_player()
        return self.observe(), False

    def initialize_game(self):
        round_board = copy.deepcopy(board)
        self.board = round_board
        self.current_player = self.board.players[0]
        self.action_space = [i for i in range(len(self.board.hexs))]
        self.reward_store = RewardStore()
        self.reward_store.initialize_store()
