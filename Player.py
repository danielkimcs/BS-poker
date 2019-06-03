from BSPokerProject.Card import Card

class Player(object):
    def __init__(self, num=1):
        self.num = num
        self.cards = []
        self.bet = None

    def increment(self):
        self.num += 1

    def get_num(self):
        return self.num

    def get_cards(self):
        return self.cards

    def empty_hand(self):
        self.cards = []

    def add_card(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def set_bet(self, bet):
        self.bet = bet

    def get_bet(self):
        return self.bet

