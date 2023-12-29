from penguin import Penguin, PenguinType
# create a player class with attributes: name, color, penguins, score, cards
class Player:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.penguins = [Penguin(PenguinType.BIG), Penguin(PenguinType.MED), Penguin(PenguinType.SMALL)]
        self.score = 0
        self.cards = []
        
    def get_name(self):
        return self.name
    def get_color(self):
        return self.color
    def get_penguins(self):
        return self.penguins
    def get_score(self):
        return self.score
    def get_cards(self):
        return self.cards
    
    def add_score(self, score):
        self.score += score
    def add_card(self, card):
        self.cards.append(card)
        
    def __str__(self):
        return f"Player: {self.name}, Color: {self.color}, Penguins: {self.penguins}, Score: {self.score}, Cards: {self.cards}"
    
    def __repr__(self):
        return f"Player: {self.name}, Color: {self.color}, Penguins: {self.penguins}, Score: {self.score}, Cards: {self.cards}"

