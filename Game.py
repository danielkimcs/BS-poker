from Deck import *
from Player import *
from Table import *

class Game(object):

    def __init__(self, num_of_players, starting_num_of_cards = 1, max_num_of_cards = 5):
        self.num_of_players = num_of_players
        self.starting_num_of_cards = starting_num_of_cards
        self.max_num_of_cards = max_num_of_cards
        self.table = Table(max_num_of_cards)
        for num in range(self.num_of_players):
            self.table.add_player(Player(starting_num_of_cards))
        self.current_player = 0
        self.table.distribute_cards()

    def get_table(self):
        return self.table