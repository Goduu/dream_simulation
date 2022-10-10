

from typing import List
from board import Board
from hex_coordinates import HexCoordinates
from movement_functions import check_movement_possibilities, mov_player
from player import Player,Hex
import numpy as np



class Observation:

    def __init__(self, observation, action_mask) -> None:
        self.observation = observation
        self.action_mask = action_mask



        

class DreamEnv:

    def __init__(self, board: Board) -> None:
        self.board = board
        self.current_player = board.players[0]
        self.action_space = [i for i in range(len(self.board.hexs))]
        self.round = 0
        self.turn = 0
        self.rounds = 3
        self.turns = 3
    
    
       
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

        action_mask = np.zeros(len(self.board.hexs), "int8")
        for mov in mov_possibilities:
            target_hex = mov.target_hex
            action_mask[target_hex.id] = 1

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

    def get_movement_by_action(self, action, mov_possibilities):

        target_hex = None
        from_hex = None
        for possibility in mov_possibilities:
            if (possibility.target_hex.id == action):
                target_hex = possibility.target_hex
                from_hex = possibility.from_hex

        return target_hex, from_hex

    def next_round(self):
        self.turn = 0
        self.round += 1
        for player in self.board.players:
            player.get_round_score()
            # player.new_round()
        # self.board.new_round()

    def restart(self):
        self.turn = 0
        self.round = 0
    
    def is_end_game(self):
        the_end = True
        for player in self.board.players:
            the_end = the_end and player.terminated
        return the_end


    def step(self, action):
        mov_possibilities = check_movement_possibilities(
            self.board, self.current_player)
        self.current_player.check_termination(mov_possibilities)

        if(not self.current_player.terminated):
            target_hex, from_hex = self.get_movement_by_action(
                action,mov_possibilities)
            if (target_hex):
                mov_player(self.board, from_hex,
                        target_hex, self.current_player.start_point)

            if(self.is_end_game()):
                if(self.round < self.rounds):
                    self.next_round()
                    return self.observe(), False
                else:
                    self.next_round()
                    return self.observe(), True

            else:
                self.next_round()
                return self.observe(), False
        else:
            if(self.is_end_game()):
                if(self.round < self.rounds):
                    self.next_round()
                    return self.observe(), False
                else:
                    self.next_round()
                    return self.observe(), True
        
        return self.observe(), False


        
            

    def agent_iter(self):
        self.pass_current_player()
        return self.current_player
