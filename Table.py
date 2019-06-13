from Card import Card
from Deck import Deck
from Player import Player

class Table(object):
    def __init__(self, max_player_cards):
        self.deck = Deck()
        self.players = []
        self.max_player_cards = max_player_cards

    def add_player(self, player):
        assert isinstance(player, Player)
        self.players.append(player)

    def get_players(self):
        return self.players

    def remove_player(self, index):
        self.players.pop(index)

    def distribute_cards(self):
        for player in self.players:
            for i in range(player.get_card_count()):
                player.add_card(self.deck.remove_card())

    def collect_cards(self):
        for player in self.players:
            player.empty_hand()
        self.deck.reset()

    # refer to method in deck
    def contains(self, hand_type, rank_bound, rank_bound2=None, count_bound=None, suit_bound=None):
        return self.deck.contains(hand_type, rank_bound, rank_bound2, count_bound, suit_bound)
