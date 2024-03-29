from Card import Card

class Player(object):
    def __init__(self, card_count=1):
        self.card_count = card_count
        self.cards = []

    def increment_card_count(self):
        self.card_count += 1

    def get_card_count(self):
        return self.card_count

    def get_cards(self):
        return self.cards

    def empty_hand(self):
        self.cards = []

    def add_card(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def printHand(self):
        for card in self.get_cards():
            print(card, end=" ")

    def __str__(self):
        st = "Card Count: "+str(self.card_count)+"; Cards: "
        for i in self.cards: st += str(i) + ", "
        return st