import hashlib
import random
import dream_v1
import numpy as np
from collections import defaultdict


def policy(observation, agent):
    possible_actions = np.flatnonzero(observation['action_mask'])
    if(len(possible_actions) == 0):
        return None
    action = random.choice(possible_actions)
    return action

# nA, number of actions
# Q, the list of Q-table dictionaries for both players, indexed by agent and by state
# agent, the agent currently acting
# action_mask, containing the available actions in the current state
# state , the hash of the current state
# eps, the value of the exploration parameter epsilon
# Q[agent][state][action_mask == 1]


def epsilon_greedy_policy(nA, Q, agent, action_mask, state, eps):
    return


def encode_state(observation):
    # encode observation as bytes
    obs_bytes = str(observation).encode('utf-8')
    # create md5 hash
    m = hashlib.md5(obs_bytes)
    # return hash as hex digest
    state = m.hexdigest()
    return (state)

# encode_state(observation['observation'])


if __name__ == '__main__':
    env = dream_v1.env(render_mode="ansi")

    env.reset()

    Q = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: np.zeros(nA)))))



    for agent in env.agent_iter():
        observation, reward, terminated, truncated, info = env.last()
        action = policy(observation, agent) if not terminated and not truncated else None
        env.step(action)
        print('obs', observation['observation'])
        print('reward', reward)
        encoded_state = encode_state(observation['observation'])
        Q[agent][encoded_state][action] = reward
        
        if (terminated and truncated):
            print('Game OVER')
            env.step(None)
            

    print(Q)
