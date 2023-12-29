

from enum import Enum

## create a class cards with attributes: target, action, timing. Target has 3 options: current_player, all_players, other_players. Action has some options: extra_move, extra_ice, extra_fishing_net, transmute_ice_fish, change direction. Timing has 5 options: breaking_ice, colliding, buying_card, playing_card, collecting
class CardTarget(Enum):
    CURRENT = "current_player"         # affect just the current player
    ALL = "all_players"                # affect all players
    OTHERS = "other_players"           # affect all players except the current player

class CardEffect(Enum):
    EXTRA_MOVE = "extra_move"
    EXTRA_ICE = "extra_ice"
    EXTRA_FISHING_NET = "extra_fishing_net"
    TRANSMUTE_ICE_FISH = "transmute_ice_fish"
    CHANGE_DIRECTION = "change_direction"
    
class CardTiming(Enum):
    BREAKING_ICE = "breaking_ice"
    COLLIDING = "colliding"
    BUYING_CARD = "buying_card"
    PLAYING_CARD = "playing_card"
    COLLECTING = "collecting"

    
class Cards:
    def __init__(self, target: CardTarget, effect: CardEffect, timing: CardTiming, scorePoints, cost):
        self.target = target
        self.effect = effect
        self.timing = timing
        self.points = scorePoints
        self.cost = cost
    

