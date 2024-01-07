import functools
from typing import List
from all_cards import get_all_cards
from classes.player import Player
from classes.backpack_item import BackpackItem, FishType, Ice
from classes.card import Card
from constants import Dir
from get_possible_actions import get_possible_actions
from game import SlideGame
from possible_actions_mapping import (
    get_action_index_by_action,
    get_possible_actions_mapping,
)

import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete, Dict, Box, MultiBinary

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
        - possible_agents
        - render_mode

        Note: as of v1.18.1, the action_spaces and observation_spaces attributes are deprecated.
        Spaces should be defined in the action_space() and observation_space() methods.
        If these methods are not overridden, spaces will be inferred from self.observation_spaces/action_spaces, raising a warning.

        These attributes should not be changed after initialization.
        """
        self.n_players = 4
        self.possible_agents = ["player_" + str(r) for r in range(self.n_players)]
        self.render_mode = render_mode
        self.game = SlideGame(self.n_players)
        self.max_actions = 5
        self.penguin_per_player = 3
        self.all_cards = get_all_cards()

        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        self.possible_actions_mapping = get_possible_actions_mapping()

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return Dict(
            {
                "action_mask": MultiDiscrete(
                    [len(self.possible_actions_mapping)]
                    * self.penguin_per_player
                ),
                "observation": Dict({
                "cards": MultiBinary(self.all_cards.__len__()),
                "terminated": Discrete(2),
                "season": Discrete(3),
                "penguins": Dict(
                    {
                        "penguins": Dict(
                            {
                                penguin_id: Dict(
                                    {
                                        "movement_tokens": Box(
                                            low=0,
                                            high=10,
                                            shape=(1,),
                                            dtype=np.int8,
                                        ),
                                        "fishing_tokens": Box(
                                            low=0,
                                            high=10,
                                            shape=(1,),
                                            dtype=np.int8,
                                        ),
                                        "direction": Discrete(6),
                                        "position": Box(
                                            low=-3,
                                            high=3,
                                            shape=(3,),
                                            dtype=np.float32,
                                        ),
                                        "ice_tokens": Discrete(10),
                                        "cards": MultiBinary(self.all_cards.__len__()),
                                        "terminated": Discrete(2),
                                        "backpack": Dict(
                                            {
                                                "ice": Discrete(10),
                                                "fish": MultiDiscrete([3, 10]),
                                            }
                                        ),
                                    }
                                )
                                for penguin_id in range(3)
                            }
                        )
                    }
                ),
                })
            }
        )

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return MultiDiscrete(
            [self.max_actions  * len(self.possible_actions_mapping)]
            * self.penguin_per_player 
           
        )

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
        self.agents = self.possible_agents[:]
        self.game = SlideGame(self.n_players)
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {agent: self.build_state_for_agent(agent) for agent in self.agents}
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def calculate_rewards(self):
        rewards = []

        for player in self.game.players:
            player_cards_points = sum([card.points for card in player.cards])
            player_penguin_cards_points = sum(
                [card.points for penguin in player.penguins for card in penguin.cards]
            )

            rewards.append(player_cards_points + player_penguin_cards_points)

        return tuple(rewards)

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

    def get_penguin_direction_encoding(self, penguin_direction: Dir):
        direction_encoding = [
            1 if direction == penguin_direction else 0 for direction in Dir
        ]
        return direction_encoding

    def get_card_encoding(self, player_cards: List[Card]):
        card_encoding = [1 if card in player_cards else 0 for card in self.all_cards]
        return np.array(card_encoding)

    def build_state_for_agent(self, agent: str):
        player: Player = next((player for player in self.game.players if player.id == agent), None)
        
        state = {
            "action_mask": self.get_action_mask(player),
            "observation":{
                "cards": self.get_card_encoding(player.cards),
                "terminated": player.terminated,
                "season": player.season,
                "penguins": {
                    "penguins": {
                        penguin_id: {
                            "movement_tokens": penguin.movement_tokens,
                            "fishing_tokens": penguin.fishing_tokens,
                            "direction": self.get_penguin_direction_encoding(
                                penguin.direction
                            ),
                            "position": penguin.position,
                            "ice_tokens": penguin.ice_tokens,
                            "cards": self.get_card_encoding(penguin.cards),
                            "terminated": penguin.terminated,
                            "backpack": self.get_penguin_backpack_encoding(
                                penguin.backpack
                            ),
                        }
                        for penguin_id, penguin in enumerate(player.penguins)
                    }
                },
                
            },
        }

        return state

    def get_action_mask(self, player: Player):
        action_mask_vector = []

        for penguin in player.penguins:
            possible_actions = get_possible_actions(
                player, penguin, self.game.board, self.game.card_market, self.game.players
            )

            sub_mask = np.zeros(len(self.possible_actions_mapping) * self.max_actions, dtype=np.int8)

            for actions in possible_actions:
                for action in actions:
                    action_index = get_action_index_by_action(action)
                    sub_mask[action_index] = 1

            action_mask_vector.append(sub_mask)

        return np.concatenate(action_mask_vector)

    def step(self, action):
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
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            # self._was_dead_step(action)
            return

        agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = self.build_state_for_agent(agent)

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            (
                self.rewards[self.agents[0]],
                self.rewards[self.agents[1]],
                self.rewards[self.agents[2]],
                self.rewards[self.agents[3]],
            ) = self.calculate_rewards()

            self.num_moves += 1
            # The truncations dictionary must be updated for all players.
            self.truncations = {
                agent: self.game.players[agent].all_penguins_terminated()
                for agent in self.agents
            }

            # observe the current state
            for i in self.agents:
                self.observations[i] = self.state[
                    self.agents[1 - self.agent_name_mapping[i]]
                ]
        else:
            # necessary so that observe() returns a reasonable observation at all times.
            self.state[self.agents[1 - self.agent_name_mapping[agent]]] = None
            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()
