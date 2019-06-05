from Card import Card
from Deck import Deck
from Player import Player
from Table import Table

t = Table(5)
for i in range(20):
    p = Player()
    t.add_player(p)

t.distribute_cards()
for i in t.deck.deck:
    print(i)

print("test single" + "-"*10)
for i in range(3,15):
    print(t.contains("single", i, count_bound=5))

print("test straight" + "-"*10)
for i in range(7,15):
    print(t.contains("five", rank_bound=i, rank_bound2=i-4, count_bound=5))

print("test flush" + "-"*10)
for i in range(7,15):
    for suit in ["S", "H", "C", "D"]:
        print(t.contains("five", rank_bound=i, count_bound=5, suit_bound=suit), end=", ")
    print()

print("test full house" + "-"*10)
for i in range(3,15):
    print(t.contains("full house", rank_bound=i))

print("test two pair" + "-"*10)
for i in range(3,15):
    for j in range(3, 15):
        if i != j:
            print(i, ":", j, "::", t.contains("double", rank_bound=i, rank_bound2=j))