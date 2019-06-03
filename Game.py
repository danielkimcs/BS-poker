from Deck import *
from Player import *


class Game(object):

    def __init__(self, numplayers):
        self.numPlayers = numplayers
        self.playerList = []
        for num in range(numplayers):
            self.playerList.append(Player)
        self.deck = Deck

