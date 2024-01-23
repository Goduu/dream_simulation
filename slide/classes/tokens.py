'''
Represents a token that every player can win along the game.
'''

from enum import Enum


class TokenType(Enum):
    QUICKER = "quicker"     # First to pass to season 2
    HOLDER = "holder"       # Last to finish the game
    COLLIDER = "collider"   # Player with most collisions with another penguin
    ICED = "iced"           # Player with most ice tokens at the end
    BREAKER = "breaker"     # Player that breaks most ice blocks
    BLOCKER = "blocker"     # Player that drop most ice blocks
    PUSHER = "pusher"       # Player that wins most collisions
    PUSHED = "pushed"       # Player that lost most collisions
    FISHER_A = "fisher_a"   # Player that fishes most A fish tokens
    FISHER_B = "fisher_b"   # Player that fishes most B fish tokens
    FISHER_C = "fisher_c"   # Player that fishes most C fish tokens

class Token:
    def __init__(self, token_type: TokenType):
        self.type: TokenType = token_type
