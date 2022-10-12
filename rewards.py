

import copy
import random
from typing import List
from player import Player, PlayerScore, PlayerSkillType

score_mapping = {
    0:0,
    1:1,
    2:2,
    3:3,
    4:5,
    5:7,
    6:9,
    7:11,
    8:13,
    9:15,
    10:17,
    11:19,
    12:21,
}



class Reward: 
    def __init__(self,id : int, cost,player_skill = None) -> None:
        self.id = id
        self.cost: PlayerScore = cost
        self.victory_points: int = self.get_victory_points()
        self.player_skill: PlayerSkillType = player_skill
        self.available = True

    def __repr__(self):
        return f"<Reward \n cost:{self.cost}  \n victory_points:{self.victory_points}  \n >"


    def get_victory_points(self):
        return score_mapping[self.cost.red] + score_mapping[self.cost.green] + score_mapping[self.cost.blue]

    def buy(self, player: Player):
        player.score.red -= self.cost.red
        player.score.green -= self.cost.green
        player.score.blue -= self.cost.blue
        player.score.reward += self.victory_points
        

rewards = [
    Reward(id= 0,cost = PlayerScore(3,3,3)),
    Reward(id= 1,cost = PlayerScore(0,0,10)),
    Reward(id= 2,cost = PlayerScore(0,0,11)),
    Reward(id= 3,cost = PlayerScore(0,0,12)),
    Reward(id= 4,cost = PlayerScore(0,10,0)),
    Reward(id= 5,cost = PlayerScore(0,11,0)),
    Reward(id= 6,cost = PlayerScore(0,12,0)),
    Reward(id= 7,cost = PlayerScore(10,0,0)),
    Reward(id= 8,cost = PlayerScore(11,0,0)),
    Reward(id= 9,cost = PlayerScore(12,0,0)),
    Reward(id= 10,cost = PlayerScore(0,0,9)),
    Reward(id= 11,cost = PlayerScore(9,0,0)),
    Reward(id= 12,cost = PlayerScore(0,9,0)),
    Reward(id= 13,cost = PlayerScore(8,0,0)),
    Reward(id= 14,cost = PlayerScore(0,8,0)),
    Reward(id= 15,cost = PlayerScore(0,0,8)),
    Reward(id= 16,cost = PlayerScore(0,2,7)),
    Reward(id= 17,cost = PlayerScore(2,7,0)),
    Reward(id= 18,cost = PlayerScore(7,0,2)),
    Reward(id= 19,cost = PlayerScore(6,3,0)),
    Reward(id= 20,cost = PlayerScore(0,6,3)),
    Reward(id= 21,cost = PlayerScore(3,0,6)),
    Reward(id= 22,cost = PlayerScore(5,0,4)),
    Reward(id= 23,cost = PlayerScore(4,5,0)),
    Reward(id= 24,cost = PlayerScore(0,4,5)),
    Reward(id= 25,cost = PlayerScore(0,4,4)),
    Reward(id= 26,cost = PlayerScore(4,0,4)),
    Reward(id= 27,cost = PlayerScore(4,4,0)),
    Reward(id= 28,cost = PlayerScore(4,3,0)),
    Reward(id= 29,cost = PlayerScore(0,4,3)),
    Reward(id= 30,cost = PlayerScore(3,0,4)),
    Reward(id= 31,cost = PlayerScore(2,2,2)),
    Reward(id= 32,cost = PlayerScore(1,1,1)),
    Reward(id= 33,cost = PlayerScore(4,4,4)),
    Reward(id= 34,cost = PlayerScore(2,2,1)),
    Reward(id= 35,cost = PlayerScore(2,1,2)),
    Reward(id= 36,cost = PlayerScore(1,2,2)),
    Reward(id= 37,cost = PlayerScore(1,1,2)),
    Reward(id= 38,cost = PlayerScore(2,1,1)),
    Reward(id= 39,cost = PlayerScore(1,2,1)),
]


REWARDS_ON_STORE = 8

class RewardStore: 
    def __init__(self) -> None:
        self.rewards_selling: List[Reward]
        self.rewards: List[Reward]

    def initialize_store(self):
        self.rewards = copy.deepcopy(rewards)
        self.rewards_selling = random.sample(self.rewards,REWARDS_ON_STORE)
        for reward in self.rewards_selling:
            reward.available = False

    def get_possible_buys(self,player:Player):
        possible_buys = []
        player_r,player_g,player_b = player.score.red,player.score.green,player.score.blue
        for reward in self.rewards_selling:
            reward_r,reward_g,reward_b = reward.cost.red,reward.cost.green,reward.cost.blue
            if( player_r >= reward_r and
                player_g >= reward_g and
                player_b >= reward_b
            ):
                possible_buys.append(reward)
        return possible_buys

    def buy_reward(self, player: Player, reward: Reward):
        self.rewards_selling.remove(reward)
        reward.buy(player)
        available_rewards = [rewards for rewards in self.rewards if rewards.available]
        if(len(available_rewards) > 0):
            new_reward = random.choice(available_rewards)
            self.rewards_selling.append(new_reward)
            new_reward.available = False