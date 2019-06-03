class Card(object):
    NUMS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    SUITS = ["S", "H", "C", "D"]

    def __init__(self, num, suit):
        assert num in Card.NUMS
        assert suit in Card.SUITS
        self.num = num
        self.suit = suit

    def get_num(self):
        return self.num

    def get_suit(self):
        return self.suit

    def __eq__(self, other):
        assert isinstance(other, Card)
        return self.num == 2 or (self.num == other.get_num() and self.suit == other.get_suit())

    def __lt__(self, other):
        assert isinstance(other, Card)
        return self.num < other.get_num()

    def __le__(self, other):
        assert isinstance(other, Card)
        return self.num <= other.get_num()

    def __gt__(self, other):
        assert isinstance(other, Card)
        return self.num > other.get_num()

    def __ge__(self, other):
        assert isinstance(other, Card)
        return self.num >= other.get_num()
