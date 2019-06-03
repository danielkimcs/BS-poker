from BSPokerProject.Card import Card
from BSPokerProject.Deck_New import Deck
from BSPokerProject.Player import Player

class Table(object):
    def __init__(self, max_player_cards):
        self.deck = Deck()
        self.players = []
        self.max_player_cards = max_player_cards

    def add_player(self, player):
        assert isinstance(player, Player)
        self.players.append(player)

    def distribute_cards(self):
        for player in self.players:
            for i in range(player.get_card_count()):
                player.add_card(self.deck.remove_card())

    def collect_cards(self):
        for player in self.players:
            player.empty_hand()
        self.deck.reset()

    # TODO - fix
    def contains_hand(self, cards_in_hand):
        assert isinstance(cards_in_hand, list)
        cards_on_table = []
        for player in self.players:
            cards_on_table += player.get_cards()

        return set(cards_in_hand) <= set(cards_on_table)