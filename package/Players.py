import os
import asyncio
from .Shuffle import *


class Player:
    def __init__(self, name, hand=["", ""], wallet=1000, allIn=False, points=0, status=True, bet=0):
        self.name = name
        self.hand = hand
        self.wallet = wallet
        self.allIn = allIn
        self.points = points
        self.status = status
        self.bet = bet

    def showCards(self, nbRound):
        os.system('cls' if os.name == 'nt' else 'clear')
        input(self.name + ", Appuyez sur ENTREE pour visualisez vos cartes")
        if nbRound == 1:
            print("")
        elif nbRound == 2:
            print('\n')
            printTableFlop(cardsOnTable)
        elif nbRound == 3:
            print('\n')
            printTableTurn(cardsOnTable)
        elif nbRound == 4:
            print('\n')
            printTableRiver(cardsOnTable)
        print('\n')
        print(f"Vous possédez la main {self.hand}")
        print('\n')
        input("Appuyez à nouveau sur ENTREE pour masquer vos cartes")
        os.system('cls' if os.name == 'nt' else 'clear')

    def showAllCards(self):
        print('\n')
        print(f"{self.name} possède la main {self.hand}")
        print('\n')
