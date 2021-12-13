from .Players import Player
from .Shuffle import *
from .Print import *
import time


class table:
    def __init__(self, money=0, currentBet=0):
        self.money = money
        self.currentBet = currentBet

    def Ante(self, game):  # * Petite blinde / Grosse blinde
        currentPlayer = game.currentPlayer()
        if currentPlayer.wallet > 10:
            print(
                f"{currentPlayer.name}, vous êtes de petite blinde, vous mettez donc 10€ sur la table.")
            currentPlayer.wallet -= 10
            self.currentBet = 10
            self.money += 10
            currentPlayer.bet = self.currentBet
        else:
            print(f"{currentPlayer.name}, comme vous n'avez pas assez d'argent pour la petite blinde, vous n'avez pas d'autre choix que de faire un tapis")
            self.allIn(currentPlayer)
        if game.getNextPlayer().wallet > 10:
            print(
                f"{game.getNextPlayer().name}, vous êtes de grosse blinde, vous mettez donc 20€ sur la table.")
            game.getNextPlayer().wallet -= 20
            self.currentBet = 20
            self.money += 20
            game.getNextPlayer().bet = self.currentBet
        else:
            print(f"{game.getNextPlayer().name}, comme vous n'avez pas assez d'argent pour la petite blinde, vous n'avez pas d'autre choix que de faire un tapis")
            self.allIn(game.getNextPlayer())
        game.nextPlayer()
        game.nextPlayer()

    def Bet(self, player):  # * Mise initiale
        bet = 0
        while bet <= self.currentBet:
            bet = input(f"{player.name}, Combien voulez vous miser ? :")
            try:
                bet = int(bet)
            except ValueError:
                print("Vous n'avez pas entré de nombre.\nRéessayez !")
                bet = 0
                continue
            if bet > player.wallet:
                print(
                    "Vous n'avez pas assez d'argent pour miser cette somme!")
                bet = 0
                continue
        if bet == player.wallet:
            print("Vous faites Tapis.")
            self.allIn(player)
            return
        player.wallet -= bet
        self.money += bet
        self.currentBet = bet
        player.bet = self.currentBet
        print(f"{player.name}, vous avez misé {self.currentBet}€")

    def Call(self, player):  # * Suivre
        if self.currentBet >= player.wallet:
            print(
                f"Vous suivez avec le solde de votre compte qui est de {player.wallet}€.")
            self.allIn(player)
        else:
            player.wallet -= (self.currentBet - player.bet)
            self.money += (self.currentBet - player.bet)
            player.bet = self.currentBet
            print(
                f"Vous vous alignez à la mise précédente qui est de {self.currentBet}€.")

    def Raise(self, player):  # * Relancer
        currentRaise = 0
        while currentRaise <= 0:
            currentRaise = input(
                f"{player.name}, Combien voulez vous relancer ? :")
            try:
                currentRaise = int(currentRaise)
            except ValueError:
                print("Vous n'avez pas entré de nombre.\nRéessayez !")
                currentRaise = 0
                continue
            if currentRaise > player.wallet:
                print(
                    "Vous n'avez pas assez d'argent pour miser cette somme!")
                currentRaise = 0
                continue
        print(f"Vous avez relancé de {currentRaise}€")
        self.currentBet += currentRaise
        self.money += self.currentBet
        player.wallet -= self.currentBet
        player.bet = self.currentBet

    def Check(self, player):  # * Check
        print(f"Vous décidez de ne rien faire.")

    def allIn(self, player):  # * Tapis
        if player.wallet >= self.currentBet:
            self.currentBet = player.wallet
        self.money += player.wallet
        player.wallet -= player.wallet
        player.allIn = True
        player.bet = self.currentBet

    def Fold(self, game, player):  # * Se coucher
        print(f"Vous vous couchez")
        player.status = False
        game.foldPlayer(player)

    def Choice(self, game, nbRound):
        player = game.currentPlayer()
        nbPlayer = game.Count()
        rep = ""
        for _ in range(nbPlayer):
            if game.checkFoldedPlayers():
                return
            if self.currentBet == 0 and player.allIn == False:
                roundPlayer(player)
                if nbRound == 1:
                    printEmptyTable()
                elif nbRound == 2:
                    printTableFlop(cardsOnTable)
                elif nbRound == 3:
                    printTableTurn(cardsOnTable)
                elif nbRound == 4:
                    printTableRiver(cardsOnTable)
                print(
                    f"Il n'y a pas encore de mise pour ce tour. Argent sur la table: {self.money}€")
                print(f"Vous possédez {player.wallet}€ .")
                while rep != "mise" or rep != "check" or rep != "tapis" or rep != "se coucher":
                    rep = input("Vous pouvez choisir de miser(\"mise\"), de ne rien faire(\"check\"), de faire tapis (\"tapis\"),de vous coucher (\"se coucher\") ou encore voir vos cartes (\"cartes\"). Que désirez vous faire ? : ")
                    if rep == "mise":
                        self.Bet(player)
                        break
                    elif rep == "check":
                        self.Check(player)
                        break
                    elif rep == "tapis":
                        self.allIn(player)
                        break
                    elif rep == "se coucher":
                        player.bet = 0
                        self.Fold(game, player)
                        break
                    elif rep == "cartes":
                        player.showCards(nbRound)
                    else:
                        print(
                            "Mauvaise réponse!")
            elif player.bet != self.currentBet and player.allIn == False:
                roundPlayer(player)
                if nbRound == 1:
                    printEmptyTable()
                elif nbRound == 2:
                    printTableFlop(cardsOnTable)
                elif nbRound == 3:
                    printTableTurn(cardsOnTable)
                elif nbRound == 4:
                    printTableRiver(cardsOnTable)
                print(
                    f"La mise est actuellement de {self.currentBet} €. Argent sur la table: {self.money}€ ")
                print(f"Vous possédez {player.wallet}€ .")
                while rep != "relance" or rep != "tapis" or rep != "se coucher" or rep != "suivre":
                    rep = input("Vous pouvez choisir de suivre (\"suivre\"), de relancer (\"relance\"), de faire tapis (\"tapis\"), de vous coucher (\"se coucher\") ou de voir vos cartes (\"cartes\"). Que désirez vous faire ? : ")
                    if rep == "relance":
                        self.Raise(player)
                        break
                    elif rep == "tapis":
                        self.allIn(player)
                        break
                    elif rep == "se coucher":
                        player.bet = 0
                        self.Fold(game, player)
                        break
                    elif rep == "suivre":
                        self.Call(player)
                        break
                    elif rep == "cartes":
                        player.showCards(nbRound)
                    else:
                        print(
                            "Mauvaise réponse!")
            game.nextPlayer()
            player = game.currentPlayer()
            time.sleep(1)
        for _ in range(nbPlayer):
            folded = False
            if player.allIn:
                game.nextPlayer()
                player = game.currentPlayer()
                continue
            while player.bet < self.currentBet:
                print("\n")
                print(
                    f"{player.name}, vous devez vous alligner à la mise actuelle qui est de {self.currentBet}€. Vous possédez {player.wallet}€  | Argent sur la table --> {self.money} €")
                res = ""
                while res != "oui" or res != "o" or res != "y" or res != "non" or res != "n":
                    res = input(
                        "Voulez vous vous mettre à niveau de la mise? (oui/non) : ")
                    if res == "oui" or res == "o" or res == "y":
                        print("Vous suivez.")
                        player.wallet -= (self.currentBet - player.bet)
                        self.money += (self.currentBet - player.bet)
                        player.bet = self.currentBet
                        break
                    elif res == "non" or res == "n":
                        player.bet = 0
                        self.Fold(game, player)
                        folded = True
                        break
                    else:
                        print(
                            "Mauvaise réponse! Veuillez entrer \"oui\" ou \"non\"")
                if folded:
                    break
            game.nextPlayer()
            player = game.currentPlayer()

        self.currentBet = 0
        for _ in range(nbPlayer):
            player.bet = 0
            game.nextPlayer()
            player = game.currentPlayer()

    def allInTotal(self, nbRound, game, end, deck):
        nbPlayer = game.Count()
        currentPlayer = game.currentPlayer()
        for _ in range(nbPlayer):
            currentPlayer.showAllCards()
            game.nextPlayer()
            currentPlayer = game.currentPlayer()
        if nbRound == 1:
            All(deck)
        elif nbRound == 2:
            round2(deck)
        elif nbRound == 3:
            River(deck)

    def totalMoney(self):
        return self.money

    def resetMoney(self):
        self.money = 0
