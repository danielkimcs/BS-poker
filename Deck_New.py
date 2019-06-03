import random
from BSPokerProject.Card import Card

class Deck(object):
    NUM_SUITS = 4
    NUM_TO_SUIT = {0: "S", 1: "H", 2: "C", 3: "D"}
    NUM_RANKS = 13

    def __init__(self):
        self.deck = [[0 for j in range(Deck.NUM_SUITS)] for i in range(Deck.NUM_RANKS)]
        self.shuffled_cards = random.shuffle([i for i in range(Deck.NUM_SUITS * Deck.NUM_RANKS)])
        self.cards_dealt = 0

    def remove_card(self):
        card = self.shuffled_cards[self.cards_dealt]
        self.cards_dealt += 1

        row = card / 4
        col = card % 4
        self.deck[row][col] = 1

        return Card(row + 2, Deck.NUM_TO_SUIT[col])

    def reset(self):
        self.deck = [[0 for j in range(Deck.NUM_SUITS)] for i in range(Deck.NUM_RANKS)]
        self.shuffled_cards = random.shuffle([i for i in range(Deck.NUM_SUITS * Deck.NUM_RANKS)])
        self.cards_dealt = 0
