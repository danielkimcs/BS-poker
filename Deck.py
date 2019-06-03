from BSPokerProject.Card import *
from random import *


class Deck(object):
    def __init__(self):
        self.deck = []
        for num in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
            for suit in ["S", "H", "C", "D"]:
                self.deck.append(Card(num, suit))

    def shuffle(self):
        shuffle(self.deck)
    
    def remove_card(self):
        return self.deck.pop()

    def add_card(self, card):
        self.deck.append(card)
