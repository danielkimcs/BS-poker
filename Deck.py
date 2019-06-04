import random
from Card import Card

class Deck(object):
    NUM_SUITS = 4
    NUM_TO_SUIT = {0: "S", 1: "H", 2: "C", 3: "D"}
    NUM_RANKS = 13

    def __init__(self):
        self.deck = [[0 for j in range(Deck.NUM_SUITS)] for i in range(Deck.NUM_RANKS)]
        self.shuffled_cards = [i for i in range(Deck.NUM_SUITS * Deck.NUM_RANKS)]
        random.shuffle(self.shuffled_cards)
        self.cards_dealt = 0

    def remove_card(self):
        card = self.shuffled_cards[self.cards_dealt]
        self.cards_dealt += 1

        row = int(card / 4)
        col = card % 4
        self.deck[row][col] = 1

        return Card(row + 2, Deck.NUM_TO_SUIT[col])

    def reset(self):
        self.deck = [[0 for j in range(Deck.NUM_SUITS)] for i in range(Deck.NUM_RANKS)]
        self.shuffled_cards = [i for i in range(Deck.NUM_SUITS * Deck.NUM_RANKS)]
        random.shuffle(self.shuffled_cards)
        self.cards_dealt = 0

    """
    Deck.contains - parameters:

    hand_type:  "single" - high card, pair, triple, 4, 5, 6, 7, 8
                "double" - two pair
                "five" - straight, flush, straight-flush
                "full house"

    hand_type - pretty self explanatory. The type of hand you are checking for.
    This is should be the type of the last hand before BS is called

    rank_bound - serves a few functions:
    1. in the case of highs, pairs, doubles, full houses, it is just the primary rank being searched for
    2. in the case of a flush or straight, it is the upper bound of the rank.

    rank_bound2 -
    1. in the case of two pair, it is the second rank
    2. in the case of straights, it is the lower bound of the rank

    count_bound -
    1. the number of x of a kinds (1, 2, 3, 4, ... , 7, 8)
    2. the number of cards in a straight or flush (should be 5, can be more)

    suit_bound - for flushes, the suit it is in
    """
    def contains(self, hand_type, rank_bound, rank_bound2=None, count_bound=None, suit_bound=None):
        count_wild = sum(self.deck[0])
        if hand_type == "single":
            assert rank_bound is not None and count_bound is not None
            count = sum(self.deck[rank_bound])
            return count + count_wild >= count_bound
        if hand_type == "double":
            assert rank_bound is not None and rank_bound2 is not None
            count = sum(self.deck[rank_bound])
            count2 = sum(self.deck[rank_bound2])
            return count_wild + min(count - 2, 0) + min(count2 - 2, 0) >= 0
        if hand_type == "full house":
            assert rank_bound is not None
            count = sum(self.deck[rank_bound])
            count2 = 0
            for i in range(1, Deck.NUM_RANKS):
                if i != rank_bound:
                    count2 = max(sum(self.deck[i]), count2)
            return count_wild + min(count - 3, 0) + min(count2 - 2, 0) >= 0
        # should be able to deal with straights and flushes with more than 5.
        if hand_type == "five":
            search_range = self.deck
            if suit_bound is not None:  # flush
                search_range = [list([j] for j in i) for i in zip(*self.deck)][suit_bound]
            if rank_bound2 is not None:  # straight
                search_range = search_range[max(1, rank_bound2):rank_bound+1]
            else:
                search_range = search_range[1:rank_bound+1]
            count = sum([sum(i) > 0 for i in search_range])
            return count_wild + count >= count_bound
        else:
            return None
