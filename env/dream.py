from faulthandler import is_enabled
import functools
import string
from typing import List

import gym
from classes import Board, Hex, HexCoordinates, Player
from functions import get_hex_color, get_hex_coord, get_hex_player
from movement_functions import check_movement_possibilities, mov_player
import numpy as np
from gym.spaces import Discrete, Tuple, Dict, Box

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon


p1_start_coord = HexCoordinates(0, -2, 2)
p2_start_coord = HexCoordinates(2, -2, 0)
p3_start_coord = HexCoordinates(-2, 2, 0)
p4_start_coord = HexCoordinates(0, 2, -2)
# should be other color
blue_four = Hex(0, coordinates=HexCoordinates(2, 0, -2), type="blue")
start_one = Hex(1, coordinates=p1_start_coord, type="start")
start_two = Hex(2, coordinates=p2_start_coord, type="start")
start_three = Hex(3, coordinates=p3_start_coord, type="start")
start_four = Hex(4, coordinates=p4_start_coord, type="start")

red_one = Hex(5, coordinates=HexCoordinates(-1, -1, 2), type="red")
red_two = Hex(6, coordinates=HexCoordinates(0, 0, 0), type="double-red")
red_three = Hex(7, coordinates=HexCoordinates(1, 1, -2), type="red")

blue_one = Hex(8, coordinates=HexCoordinates(2, -1, -1), type="blue")
blue_two = Hex(9, coordinates=HexCoordinates(1, 0, -1), type="double-blue")
blue_three = Hex(10, coordinates=HexCoordinates(-2, 1, 1), type="blue")

green_one = Hex(11, coordinates=HexCoordinates(1, -1, 0), type="green")
green_two = Hex(12, coordinates=HexCoordinates(-1, 0, 1), type="double-green")
green_three = Hex(13, coordinates=HexCoordinates(-1, 1, 0), type="green")

material_one = Hex(14, coordinates=HexCoordinates(0, -1, 1), type="material")
material_two = Hex(15, coordinates=HexCoordinates(0, 1, -1), type="material")

hexs = [
    start_one, start_two, start_three, start_four, red_one, red_two, red_three,
    blue_one, blue_two, blue_three, blue_four, green_one, green_two,
    green_three, material_one, material_two
]


def env(render_mode=None):
    """
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
    # env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gym, we inherit the "render_modes",
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
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.
        """
        self.agent_number = 4
        self.rounds = 3
        self.possible_agents = ["player_" +
                                str(r) for r in range(self.agent_number)]
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        # 6 options to move from a hexagon
        self.total_hexs = len(hexs)

        self.action_spaces = {i: Discrete(self.total_hexs)
                              for i in self.possible_agents}

        # Tuple (HexNumber, PlayerInIt)
        self.observation_spaces = {
            i: Dict(
                {
                    "observation": Box(
                        low=0, high=1, shape=(self.total_hexs, self.agent_number), dtype=np.int8
                    ),
                    "action_mask": Box(low=0, high=1, shape=(self.total_hexs,), dtype=np.int8),
                }
            )
            for i in self.possible_agents
        }

        self.render_mode = render_mode

    # this cache ensures that same space object is returned for the same agent
    # allows action space seeding to work as expected
    # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return self.observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return self.action_spaces[agent]

    def render(self):
        """
        Renders the environment. In human mode, it can print to terminal, open
        up a graphical window, or open up some other display that a human can see and understand.
        """
        if self.render_mode is None:
            gym.logger.WARN(
                "You are calling render method without specifying any render mode."
            )
            return

        coord = list(map(get_hex_coord, self.board.hexs))
        colors = list(map(get_hex_color, self.board.hexs))
        labels = list(map(get_hex_player, self.board.hexs))
        # Horizontal cartesian coords
        hcoord = [c.r for c in coord]

        # Vertical cartersian coords
        vcoord = [
            2. * np.sin(np.radians(60)) * (c.q - c.s) / 3. for c in coord
        ]
        fig, ax = plt.subplots(1, figsize=(8, 8))
        ax.set_aspect('equal')

        for x, y, c, l in zip(hcoord, vcoord, colors, labels):
            color = c[0]  # matplotlib understands lower case words for colours
            hex = RegularPolygon((x, y),
                                 numVertices=6,
                                 radius=2. / 3.,
                                 orientation=np.radians(30),
                                 facecolor=color,
                                 alpha=0.7,
                                 edgecolor="white" if
                                 (color == "cyan" or color == "lime"
                                  or color == "coral") else 'k')

            ax.add_patch(hex)
            # Also add a text label
            ax.text(x, y + 0.2, l[0], ha='center', va='top')
        plt.xlim([-4, 4])
        plt.ylim([-4, 4])
        plt.axis('off')
        # Add a table at the bottom of the axes
        plt.savefig(
            "./env/roundturn" +
            str(self.round) + "pname" + self.agent_selection + ".png",
            dpi='figure',
            format=None,
            metadata=None,
            bbox_inches=None,
            pad_inches=0.1,
            facecolor='auto',
            edgecolor='auto',
        )
        # plt.show()
        plt.close()

    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        current_player = self.players[0]
        for p in self.players:
            print('agent ------ observe', agent, p.name)
            if (agent == p.name):
                current_player = p
        

        mov_possibilities = check_movement_possibilities(
            self.board, current_player)

        action_mask = np.zeros(self.total_hexs, "int8")
        for mov in mov_possibilities:
            target_hex = mov["target_hex"]
            action_mask[target_hex.id] = 1

        obs_array = np.zeros([self.total_hexs, 2], "int8")
        for player in self.players:
            for occupied in player.occupied_hexagons:
                if (player.id == current_player.id):
                    obs_array[occupied.id][0] = 1
                else:
                    obs_array[occupied.id][1] = 1

        observation = np.stack(
            obs_array, axis=1).astype(np.int8)
        # observation of one agent is the previous state of the other
        # return np.array(self.observations[agent])
        return {"observation": observation, "action_mask": action_mask}

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def update_truncation_termination(self):
        truncations = {
            agent: len(check_movement_possibilities(self.board, self.players[i])) == 0 for i, agent in enumerate(self.agents)
        }
        terminations = {
            agent: self.players[i].cubes == 0 for i, agent in enumerate(self.agents)
        }
        return truncations, terminations

    def reset_round(self):

        p1 = Player(0, "player_0", start_point=start_one, cubes=3, skills=[])
        p2 = Player(1, "player_1", start_point=start_two, cubes=3, skills=[])
        p3 = Player(2, "player_2", start_point=start_three, cubes=3, skills=[])
        p4 = Player(3, "player_3", start_point=start_four, cubes=3, skills=[])
        self.players = [p1, p2, p3, p4]
        self.board = Board(hexs=hexs)

        self.round += 1
        self.turns_taken = 0
        self.agents = self.possible_agents[:]
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()
        self.rewards = {agent: 0 for agent in self.agents}
        print("--------------re", self.rewards)
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.state = {agent: 7 for agent in self.agents}
        self.observations = {agent: 7 for agent in self.agents}
        self.num_moves = 0
        for hex in self.board.hexs:
            hex.player_occupation = []
        for player in self.players:
            player.occupied_hexagons = [player.start_point]
            for i in range(player.cubes):
                player.start_point.player_occupation.append(player)

    def reset(self, seed=None, return_info=False, options=None):
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
        self.round = -1
        self.reset_round()
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}

    def get_player_by_agent_name(self, agent_name: str):
        current_player = self.players[0]
        for p in self.players:
            if (agent_name == p.name):
                current_player = p
        return current_player

    # original was dead step modified
    def __was_dead_step(self, action: None, agent: str) -> None:

        if action is not None:
            raise ValueError(
                "when an agent is dead, the only valid action is None")

        self.agents.remove(agent)

        # finds next dead agent or loads next live agent (Stored in _skip_agent_selection)
        _deads_order = [
            agent
            for agent in self.agents
            if (self.terminations[agent] or self.truncations[agent])
        ]
        if _deads_order:
            if getattr(self, "_skip_agent_selection", None) is None:
                self._skip_agent_selection = self.agent_selection
            self.agent_selection = _deads_order[0]
        else:
            if getattr(self, "_skip_agent_selection", None) is not None:
                assert self._skip_agent_selection is not None
                self.agent_selection = self._skip_agent_selection
            self._skip_agent_selection = None
        self._clear_rewards()

    def is_end_round(self, action):
        end_round = True
        for i in self.agents:
            end_round = end_round and (
                self.truncations[i] or self.terminations[i]) 
        if end_round:
            # rewards for all agents are placed in the .rewards dictionary
            for agent in self.agents:
                agent_player = [player for player in self.players].index(agent)
                self.rewards[agent
                             ] = self.players[agent_player].get_round_score()

            self.num_moves += 1
            # The truncations dictionary must be updated for all players.
            self.truncations, self.terminations = self.update_truncation_termination()

            # observe the current state
            for agent_observed in self.agents:
                self._was_dead_step(action, agent_observed)
        return end_round

    # if he was pushed to a start point
    def revive_agent_check(self, agent):
        # if he was pushed to a start point
        for possible_agent in self.agents:
            player_to_check = self.get_player_by_agent_name(possible_agent)
            if (self.terminations[possible_agent] and player_to_check.cubes > 0):
                print("revive ", player_to_check.name)
                self.terminations[possible_agent] = False
                self.agents.append(agent)

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

        agent = self.agent_selection

        current_player = self.get_player_by_agent_name(agent)
        print('currentplayer name', current_player.name, agent)

        action is not None and self.revive_agent_check(agent)

        if (
            self.terminations[agent]
            or self.truncations[agent]
        ):
            print('terminou ou truncou', self.agents)
            print('terminou ou truncou', agent)
            print('terminou ou truncou acg', action)

            self.__was_dead_step(None, agent)

        
        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        # self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[agent] = action

        # collect reward if it is the last agent to act
        is_end_round = self.is_end_round(action)
        print("========================================================", is_end_round)
        if (not is_end_round):

            self._clear_rewards()

            target_hex, from_hex = self.chose_mov_action(
                action, current_player)
            if (target_hex):
                mov_player(self.board, from_hex,
                           target_hex, current_player.start_point)
                # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()
        self.truncations, self.terminations = self.update_truncation_termination()

        print("[ist_end_round]-------------------------------------------------------------------", is_end_round,self.round)
        if self.render_mode == "human":
            self.render()

       
        if is_end_round:
            if self.rounds < self.round:
                print("[RESETOU]-------------------------------------------------------------------", self.round)
                self.reset_round()

    def chose_mov_action(self, action, player):
        mov_possibilities = check_movement_possibilities(
            self.board, player)

        target_hex = None
        from_hex = None
        for possibility in mov_possibilities:
            if (possibility["target_hex"].id == action):
                target_hex = possibility["target_hex"]
                from_hex = possibility["from_hex"]

        return target_hex, from_hex
