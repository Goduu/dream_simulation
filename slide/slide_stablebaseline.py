from typing import List, Tuple
from all_cards import get_all_cards
from classes.player import Player
from classes.backpack_item import BackpackItem, FishType, Ice
from classes.card import Card
from constants import Dir
from classes.penguin import Penguin
from classes.action import ActionType
from printc import MColors, printc
from get_possible_actions import get_possible_actions
from game import SlideGame
from possible_actions_mapping import (
    get_action_by_index,
    get_action_index_by_action,
    get_possible_actions_mapping,
)

import numpy as np
from gymnasium.spaces import  MultiDiscrete, Dict, Box

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers


def env(render_mode=None):
    """
    https://pettingzoo.farama.org/content/environment_creation/
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    if render_mode == "ansi":
        env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human"], "name": "rps_v2"}

    def __init__(self, render_mode=None):
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - agents
        - render_mode

        Note: as of v1.18.1, the action_spaces and observation_spaces attributes are deprecated.
        Spaces should be defined in the action_space() and observation_space() methods.
        If these methods are not overridden, spaces will be inferred from self.observation_spaces/action_spaces, raising a warning.

        These attributes should not be changed after initialization.
        """
        self.n_players = 4
        self.max_items = 10
        self.agents = ["player_" + str(r) for r in range(self.n_players)]
        self.possible_agents = self.agents[:]
        self.render_mode = render_mode
        self.game = SlideGame(self.n_players)
        self.max_actions = 5
        self.penguin_per_player = 3
        self.all_cards = get_all_cards()
        self.possible_actions_mapping = get_possible_actions_mapping()
        self.agent_name_mapping = dict(zip(self.agents, list(range(len(self.agents)))))
        self.action_spaces = {
            agent: MultiDiscrete(
                [len(self.possible_actions_mapping)]
                * self.penguin_per_player
                * self.max_actions
            )
            for agent in self.agents
        }

        self.observation_spaces = {
            agent: Dict(
                {
                    "action_mask": Box(
                        low=0,
                        high=1,
                        shape=(
                            self.penguin_per_player * self.max_actions,
                            len(self.possible_actions_mapping),
                        ),
                        dtype=np.int8,
                    ),
                    "observation": Box(
                                low=-10,
                                high=10,
                                shape=(128,),
                                dtype=np.float32,
                            ),
                }
            )
            for agent in self.agents
        }

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    def observation_space(self, agent):
        return self.observation_spaces[agent]

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    def action_space(self, agent):
        return self.action_spaces[agent]

    def render(self):
        for player in self.game.players:
            player.print_penguins()

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return self.observations[agent]

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.agents = self.agents[:]
        self.game = SlideGame(self.n_players)
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {
            agent: self.build_state_for_agent(agent) for agent in self.agents
        }
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def calculate_rewards(self, player):
        player_cards_points = sum([card.points for card in player.cards])
        player_penguin_cards_points = sum(
            [card.points for penguin in player.penguins for card in penguin.cards]
        )

        return player_cards_points + player_penguin_cards_points

    def get_penguin_backpack_encoding(self, penguin_backpack: List[BackpackItem]):
        zeros = np.zeros((self.max_items,), dtype=np.int8)
        fish = [
            1
            if item.type == FishType.A
            else 2
            if item.type == FishType.B
            else 3
            if item.type == FishType.C
            else 4
            if item == Ice()
            else 0
            for item in penguin_backpack
        ]

        fish.extend(zeros[len(fish) :])
        return np.array(fish, dtype=np.int8)

    def get_penguin_direction_encoding(self, penguin_direction: Dir):
        for index, d in enumerate(Dir):
            if d == penguin_direction:
                return index + 1
        return 0

    def get_card_encoding(self, player_cards: List[Card]):
        card_encoding = [1 if card in player_cards else 0 for card in self.all_cards]
        return np.array(card_encoding, dtype=np.int8)

    def get_position_encoding(self, position: Tuple[int, int, int]):
        if position is None:
            return np.array([-3, -3, -3], dtype=np.float32)
        return np.array(position, dtype=np.float32)

    def build_state_for_agent(self, agent: str):
        player: Player = next(
            (player for player in self.game.players if player.id == agent), None
        )
        all_penguins_possible_actions = {
            penguin_id: [] for penguin_id, _ in enumerate(player.penguins)
        }
        all_action_masks = []
        for penguin_id, penguin in enumerate(player.penguins):
            action_mask, possible_actions_array = self.get_action_mask(player, penguin)
            print("action_mask", action_mask)
            all_penguins_possible_actions[penguin_id].append(possible_actions_array)
            for action_in_mask in action_mask:
                all_action_masks.append(action_in_mask)

        state = {
            # "possible_actions_array": all_penguins_possible_actions,
            "action_mask": tuple(all_action_masks),
            "observation": {
                "cards": self.get_card_encoding(player.cards),
                "terminated": 1 if player.terminated else 0,
                "season": player.season,
                **{
                    f"p{penguin_id}_{attr}": value
                    for penguin_id, penguin in enumerate(player.penguins)
                    for attr, value in {
                        "movement_tokens": penguin.movement_tokens,
                        "fishing_tokens": penguin.fishing_tokens,
                        "direction": self.get_penguin_direction_encoding(
                            penguin.direction
                        ),
                        "position": self.get_position_encoding(penguin.position),
                        "ice_tokens": penguin.ice_tokens,
                        "cards": self.get_card_encoding(penguin.cards),
                        "terminated": 1 if penguin.terminated else 0,
                        "backpack": self.get_penguin_backpack_encoding(
                            penguin.backpack
                        ),
                    }.items()
                },
            },
        }
        state["observation"] = self.flatten_observations(state["observation"])
        return state
    
    def flatten_observations(self, observation):
        """
        Flattens the observation dictionary into an array of numbers.
        """
        value_list = list(observation.values())
        #for every value in value_list, if its an array, flatten it, if it is a number append it to result
        result = []
        for value in value_list:
            if type(value) == np.ndarray:
                result.extend(value)
            else:
                result.append(value)
                
        return result

    def get_action_mask(self, player: Player, penguin: Penguin):
        possible_actions = get_possible_actions(
            player, penguin, self.game.board, self.game.card_market, self.game.players
        )

        first_action_mask_vector = np.zeros(
            len(self.possible_actions_mapping), dtype=np.int8
        )
        second_action_mask_vector = np.zeros(
            len(self.possible_actions_mapping), dtype=np.int8
        )
        third_action_mask_vector = np.zeros(
            len(self.possible_actions_mapping), dtype=np.int8
        )
        fourth_action_mask_vector = np.zeros(
            len(self.possible_actions_mapping), dtype=np.int8
        )
        fifth_action_mask_vector = np.zeros(
            len(self.possible_actions_mapping), dtype=np.int8
        )

        possible_actions_array = []
        for actions in possible_actions:
            order = []
            for action in actions:
                action_index = get_action_index_by_action(action)
                order.append(action_index)
            possible_actions_array.append(order)

        for actions in possible_actions:
            for index, action in enumerate(actions):
                action_index = get_action_index_by_action(action)
                if index == 0:
                    first_action_mask_vector[action_index] = 1
                elif index == 1:
                    second_action_mask_vector[action_index] = 1
                elif index == 2:
                    third_action_mask_vector[action_index] = 1
                elif index == 3:
                    fourth_action_mask_vector[action_index] = 1
                elif index == 4:
                    fifth_action_mask_vector[action_index] = 1
                    
        return (
            tuple(np.stack(
                [
                    first_action_mask_vector,
                    second_action_mask_vector,
                    third_action_mask_vector,
                    fourth_action_mask_vector,
                    fifth_action_mask_vector,
                ]
            )),
            possible_actions_array,
        )

    def take_penguin_actions(self, actions, player: Player):
        for action_index, action_id in enumerate(actions):
            penguin_id = action_index // self.max_actions
            action_order = action_index - penguin_id * self.max_actions
            penguin = next(
                (
                    penguin
                    for penguin_idx, penguin in enumerate(player.penguins)
                    if penguin_idx == penguin_id
                ),
                None,
            )
            if not penguin:
                printc(f"Penguin does not exist.", MColors.FAIL)
                return {}, {}, {}, {}, {}

            action = get_action_by_index(action_id)
            self.game.handle_action(player, penguin, action)
            # pass season index is 0, if a penguin pass season, the other ones
            # would also pass
            if action.type == ActionType.PASS_SEASON:
                break

    def step(self, actions):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        agent = self.agent_selection
        player = next(
            (player for player in self.game.players if player.id == agent), None
        )

        if self.terminations[agent] or self.truncations[agent]:
            self._was_dead_step(actions)
            return

        if not player:
            printc(f"Player {agent} does not exist.", MColors.FAIL)
            return {}, {}, {}, {}, {}
        self.take_penguin_actions(actions, player)

        if self.game.check_game_over():
            winner = self.game.check_winner()
            if winner is not None:
                winner_player = next(
                    (player for player in self.game.players if player.id == winner),
                    None,
                )
                printc(
                    f"Player {winner} won the game with: {winner_player.score()}",
                    MColors.YELLOW,
                )
                self.rewards[winner] += 100
            else:
                printc(
                    f"It was a draw! Scores: {[{player.id: player.score()} for player in self.game.players]}",
                    MColors.YELLOW,
                )
            self.terminations = {i: True for i in self.agents}
            printc("Game over", MColors.OKGREEN)
        else:
            self.game.terminate_penguins_without_possible_actions(player)

        # stores state of current agent
        self.state[agent] = self.build_state_for_agent(agent)

        self.rewards[agent] += self.calculate_rewards(player)

        self.num_moves += 1

        self.observations = {
            agent: self.build_state_for_agent(agent) for agent in self.agents
        }
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()
        # selects the next agent.
        self.agent_selection = self._agent_selector.next()

        # if self.render_mode == "human":
        #     self.render()

        infos = {}
        return (
            self.observations,
            self.rewards,
            self.terminations,
            self.truncations,
            infos,
        )
