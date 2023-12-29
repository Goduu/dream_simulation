from enum import Enum
import random
from typing import Dict, List, Optional, Tuple, Union

# Coordinates for the outer hexagons
outer_hexagons = [
    (1, -1, 0), (1, 0, -1), (0, 1, -1),
    (-1, 1, 0), (-1, 0, 1), (0, -1, 1)
]

# Coordinates for the second outer hexagons
second_outer_hexagons = [
        (2, -2, 0), (2, -1, -1), (1, 1, -2),
        (-1, 2, -1), (-2, 1, 1), (-1, -1, 2),
        (1, -2, 1), (0, 2, -2), (-2, 0, 2),
        (2, 0, -2), (-2, 2, 0), (0, -2, 2)
    ]

class Hexagon:
    def __init__(self, q: int, r: int, s: int, fish_quantity: int, fish_type: str):
        self.q: int = q
        self.r: int = r
        self.s: int = s
        self.fish_quantity: int = fish_quantity
        self.fish_type: str = fish_type
        self.has_ice_block: bool = False

 # Constants for penguin types
BIG_PENGUIN = {'name': 'BIG', 'movement': 2, 'fishing': 2, 'ice': 4, 'slots': 8}
MEDIUM_PENGUIN = {'name': 'MED','movement': 3, 'fishing': 3, 'ice': 2, 'slots': 3}
SMALL_PENGUIN = {'name': 'SMALL','movement': 4, 'fishing': 2, 'ice': 1, 'slots': 6}

class Penguin:
    def __init__(self, penguin_type: dict, player_id: int):
        self.id: int = f'p{player_id}_{penguin_type["name"]}' 
        self.movement_tokens: int = penguin_type['movement']
        self.fishing_tokens: int = penguin_type['fishing']
        self.fish_tokens: list[Tuple[str, int]] = []  # List of tuples representing fish type and quantity
        self.ice_tokens: int = penguin_type['ice']
        self.backpack: list[Tuple[str, str]] = []  # List of tuples representing item type and fish type
        self.max_backpack_slots: int = penguin_type['slots']
        self.direction: Optional[str] = None  # Direction in which the penguin is moving (q,r,s,cq,cr,cs)
        self.position: Optional[Tuple[int, int, int]] = None  # Hexagon coordinates
        self.cards: List[Card] = []  # List to store penguin's cards
        self.terminated = False

class Card:
    def __init__(self, short_name: str, cost: List[Tuple[str, int]], card_type: str, passive_effect: str,on_play_effects: Dict, description: str, points: int = 0):
        self.short_name: str = short_name
        self.cost: List[Tuple[str, int]] = cost
        self.type: str = card_type
        self.effect: str = description
        self.points: int = points  # Points awarded to the player when the card is played
        self.passive_effect = passive_effect
        self.on_play_effect = on_play_effects
        
all_cards = [
        Card(short_name='BreakIceGainFish', cost=[('A', 2)], card_type='Passive',passive_effect="break_ice",on_play_effects={}, description='When breaking an ice, get one fish token', points=1),
        Card(short_name='BreakIceGainMove', cost=[('A', 2)], card_type='Passive',passive_effect="break_ice",on_play_effects={}, description='When breaking an ice, get one movement', points=1),
        Card(short_name='GainFishOnCardPlay', cost=[('A', 2)], card_type='Fishing',passive_effect="play_card",on_play_effects={}, description='When playing a card to this penguin, get one fish token', points=1),
        Card(short_name='BreakIceGainFishing', cost=[('C', 2)], card_type='Passive',passive_effect="break_ice",on_play_effects={}, description='When breaking an ice, get one fishing token', points=1),
        Card(short_name='ChangeDirectionOnCollision', cost=[('C', 2)], card_type='Passive',passive_effect="collide_penguin",on_play_effects={}, description='When colliding with a penguin, change your penguin direction', points=1),
        Card(short_name='LoseMoveGainIce', cost=[('A', 2)], card_type='Movement',passive_effect="",on_play_effects={"movement_token": -1, "ice_token":2 }, description='Lose one movement to get two ice tokens', points=1),
        Card(short_name='LoseIceGainFishing', cost=[('B', 2)], card_type='Fishing',passive_effect="",on_play_effects={"ice_token": 2, "fishing_token": 1}, description='Lose two ice to get one fishing token', points=1),
        Card(short_name='LoseMoveGainFishing', cost=[('A', 2)], card_type='Movement',passive_effect="",on_play_effects={"movement_token": -1, "fishing_token": 1}, description='Lose one movement to get one fishing token', points=1),
        Card(short_name='LoseFishingGainMove', cost=[('B', 2)], card_type='Fishing',passive_effect="",on_play_effects={"fishing_token": -1, "movement_token": 1}, description='Lose one fishing to get one movement token', points=1),
        Card(short_name='ChangeDirection', cost=[('A', 2)], card_type='Movement',passive_effect="",on_play_effects={}, description='Change penguin direction', points=1),
        Card(short_name='LoseIceGainFish', cost=[('A', 2)], card_type='Fishing',passive_effect="",on_play_effects={"ice_token": -1, "fish_token": 1}, description='Lose one ice and get one fish token', points=1),
        Card(short_name='IgnoreCollisionOnce', cost=[('C', 2)], card_type='Special',passive_effect="",on_play_effects={}, description='Ignore colliding once', points=1),
        Card(short_name='PlaceIceOnPenguins', cost=[('C', 2)], card_type='Special',passive_effect="",on_play_effects={}, description='Every player gets one ice token and needs to place it on one of its penguins', points=1),
        Card(short_name='ChooseFishForYouAndOthers', cost=[('A', 2)],passive_effect="", card_type='Fishing',on_play_effects={}, description='Get two fish tokens of your choice, the other players get one of the same', points=1),
        Card(short_name='DiscardFishForOthers', cost=[('C', 2)], card_type='Special',passive_effect="",on_play_effects={}, description='Every other player should discard a fish token', points=1),
        Card(short_name='GainMovesOnce', cost=[('A', 2)], card_type='Movement',passive_effect="",on_play_effects={"movement_token": 2}, description='Get two movement tokens once', points=1),
        Card(short_name='GainFishingOnce', cost=[('B', 2)], card_type='Fishing',passive_effect="",on_play_effects={"fishing_token": 2}, description='Get two fishing tokens once', points=1),
        Card(short_name='ExpandBackpack', cost=[('C', 2)], card_type='Special',passive_effect="",on_play_effects={"backpack": 2}, description='Expand its backpack slots by 2', points=1),
    ]

def initialize_card_market() -> List[Card]:
    all_cards

    # Select six random cards for the card market
    card_market = random.sample(all_cards, 6)

    return card_market

class Player:
    def __init__(self, player_id: int):
        self.player_id: int = player_id
        self.penguins: List[Penguin] = [Penguin(BIG_PENGUIN, player_id), Penguin(MEDIUM_PENGUIN, player_id), Penguin(SMALL_PENGUIN, player_id)]
        self.cards: List[Card] = []  # List to store player's cards
        self.terminated = False
        # Other attributes as needed

class ActionType(Enum):
    START = "start"
    MOVE = "move"
    DROP_ICE = "drop_ice"
    BUY_CARD = "buy_card"
    PLAY_CARD = "play_card"
    BREAK_ICE = "break_ice"
    FISHING = "fishing"
    
class Action:
    def __init__(self, action_type: ActionType, action_parameter):
        self.type = action_type
        self.parameter = action_parameter
    
    def __repr__(self):
        return f"\nAction: {self.type}, Parameter: {self.parameter}"


class FishyPenguinsGame:
    def __init__(self, num_players: int):
        self.players: List[Player] = [Player(player_id) for player_id in range(num_players)]
        self.current_player_index: int = 0  # Index of the current player in self.players
        self.board: List[Hexagon] = self.initialize_board()  # Function to create and return the hexagonal board
        self.card_market: List[Card] = initialize_card_market()
        self.round = 0
        # Other attributes and initialization as needed
        
    # returns True if given coordinates exists in self.board and has no ice block in it
    def check_coordinates_available(self, coordinates: Tuple[int, int, int]) -> bool:
        q,r,s = coordinates
        for hexagon in self.board:
            if hexagon.q == q and hexagon.r == r and hexagon.s == s:
                if not hexagon.has_ice_block:
                    return True
        return False
    

    def initialize_board(self) -> List[Hexagon]:
        board = []

        # Coordinates for the center hexagon
        center_hexagon = Hexagon(q=0, r=0, s=0, fish_quantity=3, fish_type='A')
        board.append(center_hexagon)

        for coordinates in outer_hexagons:
            q, r, s = coordinates
            hexagon = Hexagon(q=q, r=r, s=s, fish_quantity=2, fish_type='B')
            board.append(hexagon)

        for coordinates in second_outer_hexagons:
            q, r, s = coordinates
            hexagon = Hexagon(q=q, r=r, s=s, fish_quantity=1, fish_type='C')
            board.append(hexagon)

        return board
    
    def is_all_players_terminated(self):
        for player in self.players:
            if not player.terminated:
                return False
        return True
    
    def are_all_penguins_terminated(self, player: Player):
        for penguin in player.penguins:
            if not penguin.terminated:
                return False
        return True
    
    def move_to_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.round += 1
            print("--------------")
            print(f"New Round: {self.round}")
            print("--------------")
    
    def play_turn(self):
         
        if(self.is_all_players_terminated()):
            print("END GAME: All players terminated")
            return
        current_player = self.players[self.current_player_index]
        
        if(self.are_all_penguins_terminated(current_player)):
            print(f"All penguins terminated for player {current_player.player_id}")
            current_player.terminated = True
            self.move_to_next_player()
            return

        for penguin in current_player.penguins:
            if(not penguin.terminated):
                self.handle_penguin_actions(current_player, penguin)

        # Implement logic for passing to the next season, checking for game end conditions, etc.
        # You can add more game-related logic here

        # Move to the next player's turn
        self.move_to_next_player()

    def get_surroundings(self, coordinates: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        q,r,s = coordinates
        return [
            (q + 1, r - 1, s),
            (q + 1, r, s - 1),
            (q, r + 1, s - 1),
            (q - 1, r + 1, s),
            (q - 1, r,s + 1),
            (q, r - 1, s + 1),
        ]
        
    def get_hexagon(self, coordinates: Tuple[int, int, int]):
        q,r,s = coordinates
        for hexagon in self.board:
            if hexagon.q == q and hexagon.r == r and hexagon.s == s:
                return hexagon
        return None
        
    def get_adjacent_hexagons(self, coordinates: Tuple[int, int, int]) -> List[Hexagon]:
        surroundings = self.get_surroundings(coordinates)
        adjacent_hexagons = []
        for s in surroundings:
            q,r,s = s
            for hexagon in self.board:
                if hexagon.q == q and hexagon.r == r and hexagon.s == s:
                    adjacent_hexagons.append(hexagon)
        
        
    def calculate_direction(self,q1, r1, s1, q2, r2, s2):
        dq, dr, ds = q2 - q1, r2 - r1, s2 - s1

        if dq == 0 and dr == 0 and ds == 0:
            return None  # No movement

        if dq == 1 and dr == -1 and ds == 0:
            return 'cs'  # Move in the q direction
        if dq == -1 and dr == 1 and ds == 0:
            return 's'  # Move in the q direction
        if dq == 0 and dr == 1 and ds == -1:
            return 'cq'  # Move in the q direction
        if dq == 0 and dr == -1 and ds == 1:
            return 'q'  # Move in the q direction
        if dq == -1 and dr == 0 and ds == 1:
            return 'cr'  # Move in the q direction
        if dq == 1 and dr == 0 and ds == -1:
            return 'r'  # Move in the q direction

        return None  # Invalid movement

    def get_start_directions(self, coordinates: Tuple[int, int, int]) -> List[Hexagon]:
        surroundings_coordinates = self.get_surroundings(coordinates)
        # filter surroundings_coordinates to only include coordinates that exist in outer_hexagons
        directions = []
        for s_coordinates in surroundings_coordinates:
            if s_coordinates in outer_hexagons:
                dq,dr,ds = s_coordinates
                q,r,s = coordinates
                direction = self.calculate_direction(q,r,s,dq,dr,ds)
                directions.append(direction)
        
        return directions
        
            
    def get_possible_actions(self,player: Player, penguin: Penguin) -> List[List[Action]]:
        possible_actions: List[List[Action]] = []

        # Check if the penguin can move
        if penguin.movement_tokens > 0:
            if penguin.direction is not None and penguin.position is not None:
                # for every movement token left, check if the next direction exists in board if so add to possible actions
                for i in range(1,penguin.movement_tokens):
                    new_position = self.calculate_new_position(penguin.position, penguin.direction, i)
                    if self.check_coordinates_available(new_position):
                        if(penguin.ice_tokens >= i and i > 1):
                            for j in range(i):
                                if(penguin.ice_tokens >= j):
                                    possible_actions.append([
                                        Action("move", i),
                                        Action("drop_ice", j),
                                                    ])
                                        
                                else:
                                    possible_actions.append([Action("move", i)])
                        else:
                            possible_actions.append([Action("move", i)])
                    else:
                        break
            else: 
                for i in range(1,penguin.movement_tokens):
                    for coordinates in second_outer_hexagons:
                        if self.check_coordinates_available(coordinates):
                            start_directions = self.get_start_directions(coordinates)
                            for direction in start_directions:
                                actions = [Action("start", (coordinates,direction))]
                                if(i-1 > 0):
                                    actions.append(Action("move", i-1))
                                possible_actions.append(actions)

        # Check if the penguin can break ice
        if penguin.position is not None:
            adjacent_hexagons = self.get_adjacent_hexagons(penguin.position)
            if adjacent_hexagons:
                for adj_hexagon in adjacent_hexagons:
                    if adj_hexagon.has_ice_block:
                        possible_actions.append([Action("break_ice", (adj_hexagon.q,adj_hexagon.r,adj_hexagon.s))])

        # Check if the penguin can buy cards
        if self.card_market:
            for i, card in enumerate(self.card_market):
                if self.has_enough_tokens(penguin, card.cost):
                    possible_actions.append([Action("buy_card", i)])
        
        if player.cards:
            for card in player.cards:
                for action in possible_actions:
                    action.append(Action("play_card", card.short_name, penguin))
                    
        if penguin.fishing_tokens > 0:
            for actions in possible_actions:
                actions.append(Action("fishing", ""))

        return possible_actions
    
    def handle_penguin_actions(self,player: Player, penguin: Penguin):
        current_player = self.players[self.current_player_index]
        print(f"Player {current_player.player_id}'s turn for penguin at {penguin.position}")
        
        # Implement logic for player actions (move, break ice, buy card, etc.) for each penguin
        possible_actions = self.get_possible_actions(player, penguin)
        # print("Available actions: ", possible_actions)
        if not possible_actions:
            print("No actions available for this penguin.")
            penguin.terminated = True
            return
        actions = random.choice(possible_actions)
        print("Chosen actions: ", actions)
        for action in actions:
            if action.type == 'start':
                position, direction = action.parameter
                self.move_penguin_to_start_point(penguin, position, direction)
            elif action.type == 'move':
                self.move_penguin(penguin, action.parameter)
            elif action.type == 'break_ice':
                self.break_ice(penguin, action.parameter)
            elif action.type == 'buy_card':
                self.buy_card(current_player, penguin)
            elif action.type == 'fishing':
                self.fish(penguin)
            elif action.type == 'play_card':
                self.play_card(current_player, penguin, action.parameter)
            else:
                print("Invalid action. Choose again.")

    def move_penguin_to_start_point(self, penguin: Penguin, position, direction):
        penguin.position = position
        penguin.direction = direction
        print(f"Penguin moved to start point {penguin.position}")
        
    def move_penguin(self, penguin: Penguin, hexagons_to_move: int):
        if penguin.movement_tokens >= hexagons_to_move:
            # Assuming 'forward' is the valid direction
            direction = penguin.direction or 'forward'

            # Implement logic to update the penguin's position based on the chosen direction and hexagons to move
            for i in range(hexagons_to_move):
                new_position = self.calculate_new_position(penguin.position, direction, 1)

                # Check for collisions with other penguins
                collision_penguin = self.check_for_collision(new_position, penguin)
                if collision_penguin:
                    self.handle_collision(penguin, collision_penguin)
                else:
                    penguin.position = new_position
                    penguin.movement_tokens -= 1
                    print(f"Penguin {penguin.id} moved to {penguin.position}")

        else:
            print("Not enough movement tokens left for this penguin.")

    def calculate_new_position(self, current_position: Tuple[int, int, int], direction: str, hexagons_to_move: int) -> Tuple[int, int, int]:
        # Implement logic to calculate the new position based on the chosen direction and hexagons to move
        q, r, s = current_position
        if direction == 'q':
            r -= hexagons_to_move
            s += hexagons_to_move
        elif direction == 'r':
            q += hexagons_to_move
            s -= hexagons_to_move
        elif direction == 's':
            q -= hexagons_to_move
            r += hexagons_to_move
        elif direction == 'cq':
            r += hexagons_to_move
            s -= hexagons_to_move
        elif direction == 'cr':
            q -= hexagons_to_move
            s += hexagons_to_move
        elif direction == 'cs':
            q += hexagons_to_move
            r -= hexagons_to_move
        else:
            print("Invalid direction.")
            pass
        return q, r, s
    
    def check_for_collision(self, new_position: Tuple[int, int, int], moving_penguin: Penguin) -> Union[Penguin, None]:
        # Implement logic to check for collisions with other penguins
        for player in self.players:
            for other_penguin in player.penguins:
                if other_penguin != moving_penguin and other_penguin.position == new_position:
                    return other_penguin
        return None
            
    def get_direction_after_losing_collision(self, penguin: Penguin):
        direction = penguin.direction
        if direction == 'q':
            return 'r'
        if direction == 'r':
            return 's'
        if direction == 's':
            return 'q'
        if direction == 'cq':
            return 'cr'
        if direction == 'cr':
            return 'cs'
        if direction == 'cs':
            return 'cq'
        else:
            print("Invalid direction.")
            return direction
        
    def handle_collision(self, moving_penguin: Penguin, collided_penguin: Penguin):
        print(f"Collision between penguin at {moving_penguin.position} and {collided_penguin.position}")

        # Check ice tokens to determine the winner
        if moving_penguin.ice_tokens > collided_penguin.ice_tokens:
            print("Moving penguin wins the collision.")
            # Moving penguin continues in the hexagon, collided penguin is moved to an adjacent empty hexagon
            new_direction = self.get_direction_after_losing_collision(collided_penguin)
            collided_penguin.direction = new_direction
            self.move_penguin(collided_penguin, hexagons_to_move=1)
        elif moving_penguin.ice_tokens < collided_penguin.ice_tokens:
            print("Collided penguin wins the collision.")
            new_direction = self.get_direction_after_losing_collision(moving_penguin)
            moving_penguin.direction = new_direction
            # Collided penguin continues in the hexagon, moving penguin is moved to an adjacent empty hexagon
            self.move_penguin(moving_penguin, hexagons_to_move=1)
        else:
            print("It's a tie! Both penguins change direction to counter direction.")
            self.reverse_direction(moving_penguin)
            self.reverse_direction(collided_penguin)

    def reverse_direction(self, penguin: Penguin):
        # Reverse the direction of the penguin
        if penguin.direction == 'r':
            penguin.direction = 'cr'
        elif penguin.direction == 'cr':
            penguin.direction = 'r'
        elif penguin.direction == 's':
            penguin.direction = 'cs'
        elif penguin.direction == 'cs':
            penguin.direction = 's'
        elif penguin.direction == 'q':
            penguin.direction = 'cq'
        elif penguin.direction == 'cq':
            penguin.direction = 'q'

    def break_ice(self, penguin: Penguin, hexagon_with_ice: Hexagon):        
        if hexagon_with_ice and hexagon_with_ice.has_ice_block:
            print(f"Penguin at {penguin.position} breaks the ice block to an adjacent hexagon.")
            penguin.ice_tokens += 1
            hexagon_with_ice.has_ice_block = False
        else:
            print("Hexagon does not have an ice block.")
    
    def fish(self, penguin: Penguin):
        hexagon = self.get_hexagon(penguin.position)
        if penguin.position is not None and hexagon is not None:
            # Check if the penguin is in the same hexagon as the provided hexagon

            # Add the collected fish to the penguin's backpack
            # Assuming the backpack is a list, you might need to adapt based on your implementation
            for i in range(hexagon.fish_quantity):
                penguin.backpack.append(hexagon.fish_type)

            # Update the fishing tokens of the penguin
            penguin.fishing_tokens -= 1

            print(f"{hexagon.fish_quantity} {hexagon.fish_type} fish collected by Penguin {penguin.id}.")
        else: 
            print("Penguin has no postion or hexagon no found")

    def get_player_card(self, player: Player, card_short_name: str) -> bool:
        # Check if the player has the card
        for card in player.cards:
            if card.short_name == card_short_name:
                return card
        return None
    
    def play_card(self, player: Player, penguin: Penguin, card_short_name: str):
        # Check if the player has the card
        card: Card = self.get_player_card(player, card_short_name)
    
        if card is not None:
            # Remove the card from the player's hand
            player.cards.remove(card)

            # Add the card to the penguin's cards
            penguin.cards.append(card)

            # Check if the card has an effect
            if "ice_token" in card.on_play_effect:
                penguin.ice_tokens += card.on_play_effect["ice_token"]
                penguin.backpack.append(("ice", "ice"))
            if "movement_token" in card.on_play_effect:
                penguin.movement_tokens += card.on_play_effect["movement_token"]
            if "fishing_token" in card.on_play_effect:
                penguin.fishing_tokens += card.on_play_effect["fishing_token"]
            if "fish_token" in card.on_play_effect:
                penguin.fish_tokens.append(("A", card.on_play_effect["fish_token"]))
                penguin.backpack.append(("fish", "A"))
            if "backpack" in card.on_play_effect:
                penguin.max_backpack_slots += card.on_play_effect["backpack"]
                

    def buy_card(self, player: Player,penguin: Penguin, card_index: int):
        if 0 <= card_index < len(self.card_market):
            selected_card = self.card_market[card_index]

            # Check if the player has enough tokens to buy the card
            if self.has_enough_tokens(penguin, selected_card.cost):
                # Deduct the cost tokens from the player's penguin
                self.deduct_cost_tokens(penguin, selected_card.cost)

                # Give the card to the player
                player.cards.append(selected_card)

                # Remove the card from the market
                self.card_market.pop(card_index)

                # Add another random card to the market
                new_card = random.choice(all_cards)
                self.card_market.append(new_card)

    def has_enough_tokens(self, penguin: Penguin, cost: List[Tuple[str, int]]) -> bool:
        # Check if the player has enough tokens to buy the card
        current_in_slots: Dict[str, int] = {}
        for fish_token in penguin.fish_tokens:
            current_in_slots[fish_token.fish_type] = current_in_slots.get(fish_token.fish_type, 0) + 1
            
        for fish_type, quantity in cost:
            if current_in_slots.get(fish_type, 0) < quantity:
                return False
        return True

    def deduct_cost_tokens(self, penguin: Penguin, cost: List[Tuple[str, int]]):
        # Deduct the cost tokens from the player's penguin
        for fish_type, quantity in cost:
            for fish_token in penguin.fish_tokens:
                if fish_token.fish_type == fish_type:
                    fish_token.quantity -= quantity
                # remove the fish_token from the backpack_slots
                for item in penguin.backpack:
                    if item.type == fish_type:
                        penguin.backpack.remove(item)
                        break
                
                



