class Card(object):
    RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SUITS = ["S", "H", "C", "D"]

    def __init__(self, rank, suit):
        assert rank in Card.RANKS
        assert suit in Card.SUITS
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def get_suit(self):
        return self.suit

    def __eq__(self, other):
        assert isinstance(other, Card)
        return self.rank == other.get_rank() and self.suit == other.get_suit()

    def __lt__(self, other):
        assert isinstance(other, Card)
        return self.rank < other.get_rank()

    def __le__(self, other):
        assert isinstance(other, Card)
        return self.rank <= other.get_rank()

    def __gt__(self, other):
        assert isinstance(other, Card)
        return self.rank > other.get_rank()

    def __ge__(self, other):
        assert isinstance(other, Card)
        return self.rank >= other.get_rank()
