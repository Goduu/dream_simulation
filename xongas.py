

import hashlib
import random
from data_collector import DataCollector
from dream_env import DreamEnv, Observation
import numpy as np
from hex_coordinates import HexCoordinates
import numpy as np

data_collector = DataCollector()


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


for i in range(1000):
    env = DreamEnv()
    env.initialize_game()

    end_game = False
    observation = env.observe()
    while not end_game:
        
        action = random_policy(observation)
        observation, end_game = env.step(action)
        
        # env.pass_current_player()
        # env.board.plot_board(i, env.current_player.name)

    data_collector.collect(env.board.players)
    i +=1

    if(i % 100 == 0): print(i)


data_collector.plot_resource_analysis()
data_collector.plot_player_analysis()


