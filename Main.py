import asyncio
import os
import time
import sys
from package.Game import wholeGame
from package.Players import Player
from package.Shuffle import *
from package.Ending import endGame
from package.Money import table
from package import Print

table = table()
end = endGame()
game = wholeGame()

nbPlayer = game.initGame()
currentPlayer = game.currentPlayer()

Print.startGame()

n = 1
while nbPlayer > 1:

    Print.nbRound(n)
    time.sleep(1)

    deck = shuffleCards()
    dealCards(deck, game)

    table.resetMoney()

    tab = []
    for i, _ in enumerate(game.sleepingPlayers()):
        tab.append(game.sleepingPlayers()[i])
    for player in tab:
        game.wakeUp(player)

    for _ in range(nbPlayer):
        currentPlayer.allIn = False
        game.nextPlayer()
        currentPlayer = game.currentPlayer()

    for a in range(nbPlayer):
        game.promptCards(currentPlayer)
        print("\n")
        game.nextPlayer()
        currentPlayer = game.currentPlayer()

    table.Ante(game)
    table.Choice(game, 1)

    if game.checkFoldedPlayers():
        currentPlayer = game.currentPlayer()
        end.forfaitWinner(currentPlayer, table.totalMoney())

    elif game.checkAllIn():
        table.allInTotal(1, game, end, deck)
        print(f"Argent sur la table: {table.totalMoney()} €")
        end.finalCheck(game)
        end.whoWon(game, table.totalMoney())

    else:
        Flop(deck)
        table.Choice(game, 2)

        if game.checkFoldedPlayers():
            currentPlayer = game.currentPlayer()
            end.forfaitWinner(currentPlayer, table.totalMoney())

        elif game.checkAllIn():
            table.allInTotal(2, game, end, deck)
            print(f"Argent sur la table: {table.totalMoney()} €")
            end.finalCheck(game)
            end.whoWon(game, table.totalMoney())

        else:
            Turn(deck)
            table.Choice(game, 3)

            if game.checkFoldedPlayers():
                currentPlayer = game.currentPlayer()
                end.forfaitWinner(currentPlayer, table.totalMoney())

            elif game.checkAllIn():
                table.allInTotal(3, game, end, deck)
                print(f"Argent sur la table: {table.totalMoney()} €")
                end.finalCheck(game)
                end.whoWon(game, table.totalMoney())

            else:
                River(deck)
                table.Choice(game, 4)

                if game.checkFoldedPlayers():
                    currentPlayer = game.currentPlayer()
                    end.forfaitWinner(currentPlayer, table.totalMoney())

                else:
                    Print.endOfRound()
                    printTableRiver(cardsOnTable)

                    for _ in range(nbPlayer):
                        currentPlayer.showAllCards()
                        game.nextPlayer()
                        currentPlayer = game.currentPlayer()
                    print(f"Argent sur la table: {table.totalMoney()} €")
                    end.finalCheck(game)
                    end.whoWon(game, table.totalMoney())

    toKill = []
    nbKill = 0
    for a in range(nbPlayer):
        if currentPlayer.wallet == 0:
            nbPlayer -= 1
            print(
                f"{currentPlayer.name}, vous n'avez malheureusement plus d'argent, vous quittez donc la partie.")
            toKill.append(currentPlayer)
            nbKill += 1
        game.nextPlayer()
        currentPlayer = game.currentPlayer()

    if len(toKill) > 0:
        for a in range(nbKill):
            game.Kill(toKill[a])

    if nbPlayer > 1:
        res = input("Souhaitez vous quitter la partie? (\"oui\"/\"non\") : ")
        if res == "oui":
            confirm = input("Êtes-vous sûr? (\"oui\"/\"non\") : ")
            if confirm == "oui":
                break
        print("Vous continuez le jeu.")
        n += 1

print("Fin de Partie, merci d'avoir joué, à très bientôt! :D")
os.system("pause")
