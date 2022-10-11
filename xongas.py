

import hashlib
import random
from board import Board
from dream_env import DreamEnv, Observation
import numpy as np
from hex_coordinates import HexCoordinates

from player import Hex, Player



def random_policy(observation: Observation):
    possible_actions = np.flatnonzero(observation.action_mask)
    if(len(possible_actions) == 0):
        return None
    action = random.choice(possible_actions)
    return action

def encode_state(observation):
    # encode observation as bytes
    obs_bytes = str(observation).encode('utf-8')
    # create md5 hash
    m = hashlib.md5(obs_bytes)
    # return hash as hex digest
    state = m.hexdigest()
    return (state)




env = DreamEnv()
env.initialize_game()

end_game = False
i = 0
observation = env.observe()
while not end_game:
    
    action = random_policy(observation)
    observation, end_game = env.step(action)
    
    # env.pass_current_player()
    # env.board.plot_board(i, env.current_player.name)
    i +=1


for player in env.board.players:
    print(player.name)
    print(player.score)

