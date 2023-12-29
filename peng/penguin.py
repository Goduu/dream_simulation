from typing import List
import random
import uuid
from movement_functions import get_next_hex_coord
from hex import Hex, find_hex_by_coordinates
from enum import Enum

class PenguinType(Enum):
    BIG = "big"               # Push two in a row and stay in the first hex
    MED = "med"               # Push in empty boarder
    SMALL = "small"           # Reset an adjacent player


##create a variable to story the penguins initial attribute for each PenguinType, the attributes are: movement, fishNet and iceBlocks
class PenguinInitialAttributes:
   def __init__(self, type: PenguinType):
       #for each type set the attributes
         if type == PenguinType.BIG:
              self.movement = 2
              self.fishNet = 2
              self.iceBlocks = 4
              self.storage = 7
         elif type == PenguinType.MED:
              self.movement = 3
              self.fishNet = 2
              self.iceBlocks = 2
              self.storage = 4
         elif type == PenguinType.SMALL:
              self.movement = 4
              self.fishNet = 3
              self.iceBlocks = 1
              self.storage = 4
              
       
       
   def get_movement(self):
       return self.movement
   def get_fishNet(self):
       return self.fishNet
   def get_iceBlocks(self):
       return self.iceBlocks
   
   
   


class Penguin:
    def __init__(self, type: PenguinType) -> None:
        self.id = uuid.uuid4()
        self.type = type
        self.position: Hex
        self.equippedCards = list()
        self.attributes = PenguinInitialAttributes(type)
        self.movement = self.attributes.get_movement()
        self.fishNet = self.attributes.get_fishNet()
        self.iceBlocks = self.attributes.get_iceBlocks()
        self.nextHex: Hex = None
    
    def __eq__(self, other):
        if isinstance(other, Penguin):
            return self.id is other.id
        return NotImplemented
    
    def __repr__(self):
        return f"<Penguin id:{self.id} type: {self.type}, position: {self.position}>"
        
    # Set the new position; set the nextHex as random if none set; set nextHex as the next in the sequence
    def set_position(self, position: Hex, board_hexes: List[Hex]):
        if not self.nextHex:
            surroundings = position.get_surroundings()
            next_hex_coord = random.choice(surroundings)
            next_hex = find_hex_by_coordinates(board_hexes,next_hex_coord)
            if(not next_hex):
                raise Exception("No next hex found")
            self.set_next_hex(next_hex)
        elif self.position:
            next_coord = get_next_hex_coord(self.position.coordinates, position.coordinates)
            for hex in board_hexes:
                if hex.coordinates == next_coord:
                    self.set_next_hex(hex)
                    
        self.position = position
        
    def set_equippedCards(self, equippedCards):
        self.equippedCards = equippedCards
    def set_movement(self, movement):
        self.movement = movement
    def set_fishNet(self, fishNet):
        self.fishNet = fishNet
    def set_iceBlocks(self, iceBlocks):
        self.iceBlocks = iceBlocks
    def set_next_hex(self, next_hex: Hex):
        self.nextHex = next_hex
        
    def get_equippedCards(self):
        return self.equippedCards
    
    def get_movement(self):
        return self.movement
    
    def get_fishNet(self):
        return self.fishNet
    
    def get_iceBlocks(self):
        return self.iceBlocks
    
    def get_next_hex(self):
        return self.nextHex
        
        