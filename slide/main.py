# Example usage
import numpy as np
from possible_actions_mapping import get_action_by_index
from printc import MColors, printc
from game import SlideGame
from ui import visualize_board

for i in range(5):
    # print("starting game...", i)
    game = SlideGame(num_players=4)
    end_game = False
    while not end_game:
        end_game = game.play_turn()


# printc("\U0001F41F", MColors.OKGREEN)
# for player in game.players:
#     player.print_penguins()

# printc("Card market:", MColors.OKGREEN)
# for card in game.card_market:
#     printc(card, MColors.OKGREEN)

# import slide_stablebaseline as sz
# import random

# for i in range(100):
#     print("starting game...", i)
#     env = sz.env()
#     env.reset(seed=42)

#     for agent in env.agent_iter():
#         observation, reward, termination, truncation, info = env.last()
#         if termination or truncation:
#             actions = None

#         else:
#             # this is where you would insert your policy
#             actions = []
#             possible_actions = observation["possible_actions_array"]
#             for key in possible_actions:
#                 if possible_actions[key] == [[]] or possible_actions[key] == []:
#                     penguin_possible_actions = []
#                 else:
#                     penguin_possible_actions = random.choice(possible_actions[key][0])
#                 for i in range(5):
#                     if i < len(penguin_possible_actions):
#                         actions.append(penguin_possible_actions[i])
#                     else:
#                         actions.append(0)
#         if actions == []:
#             env.step(np.zeros(15))
#         else:
#             env.step(actions)
#     env.close()
