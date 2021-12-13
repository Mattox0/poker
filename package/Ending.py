from .Shuffle import cardsOnTable
from .Money import table

table = table()


#! Return des fonctions:
# * Value[0] --> Retourne le nombre de points rapportés par la valeur
# * Value[1] --> Retourne la valeur gagnée
# * Value[2] --> Complément (optionnel)

class endGame:
    def __init__(self, tab=cardsOnTable):
        self.tab = tab

    def checkCards(self, player):
        check = []
        for a in range(5):
            check.append(self.tab[a])
        for i in range(2):
            check.append(player.hand[i])
        return check

    def numberCheck(self, deck):
        numbers = []
        for a in range(len(deck)):
            numbers.append(deck[a][0])
        return numbers

    def powerCheck(self, deck):
        power = []
        for a in range(len(deck)):
            power.append(deck[a][1])
        return power

    def Pair(self, player, numbers=None):
        if numbers == None:
            numbers = self.numberCheck(self.checkCards(player))
        sortedNumbers = sorted(numbers, reverse=True)
        if sortedNumbers[5:] == [1, 1]:
            sortedNumbers[5:], sortedNumbers[:5] = sortedNumbers[:5], sortedNumbers[5:]
            return 13, 1, 0
        for i in range(len(sortedNumbers)):
            if i+1 >= len(sortedNumbers):
                break
            if sortedNumbers[i] == sortedNumbers[i+1]:
                return (sortedNumbers[i] - 1), sortedNumbers[i], i
        return None

    def twoPair(self, player):
        numbers = self.numberCheck(self.checkCards(player))
        numberToPop = sorted(numbers, reverse=True)
        if numberToPop[5:] == [1, 1]:
            numberToPop[5:], numberToPop[:5] = numberToPop[:5], numberToPop[5:]
        if self.Pair(player):
            for _ in range(2):
                numberToPop.pop(self.Pair(player)[2])
            res = self.Pair(player, numberToPop)
            if res:
                return self.Pair(player)[0] + 12, [self.Pair(player)[1], res[1]]
        return None

    def Trips(self, player):
        numbers = self.numberCheck(self.checkCards(player))
        sortedNumbers = sorted(numbers, reverse=True)
        if sortedNumbers[4:] == [1, 1, 1]:
            sortedNumbers[4:], sortedNumbers[:4] = sortedNumbers[:4], sortedNumbers[4:]
            return 38, 1, 0
        trips = 0
        for i in range(len(sortedNumbers)-2):
            if sortedNumbers[i] - sortedNumbers[i+1] == 0:
                if sortedNumbers[i+1] - sortedNumbers[i+2] == 0:
                    trips = sortedNumbers[i]
                    break
        if trips:
            return trips + 24, trips, i
        return None

    def Full(self, player):  # a faire apres
        numbers = self.numberCheck(self.checkCards(player))
        numberToPop = sorted(numbers, reverse=True)
        if numberToPop[4:] == [1, 1, 1]:
            numberToPop[4:], numberToPop[:4] = numberToPop[:4], numberToPop[4:]
        if self.Trips(player):
            for _ in range(3):
                numberToPop.pop(self.Trips(player)[2])
            if self.Pair(player, numberToPop):
                return self.Trips(player)[0] + 13, [self.Trips(player)[1], self.Pair(player, numberToPop)[1]]
            return None

    def Quads(self, player):
        numbers = self.numberCheck(self.checkCards(player))
        nbQuads = numbers
        nbQuads.sort()
        quads = []
        poped = False
        for i in range(len(nbQuads)):
            count = 0
            for y in range(len(nbQuads)):
                if nbQuads[i] == nbQuads[y] and i != y:
                    count += 1
                    if count == 3:
                        quads.append(nbQuads[i])
                        poped = True
                        break
            if poped == True:
                break
        if len(quads) == 1:
            res = quads[0]
            if quads[0] == 1:
                res = 14
            return (res + 50), quads[0]
        return None

    def Straight(self, player, numbers=None):
        if numbers == None:
            numbers = self.numberCheck(self.checkCards(player))
        sortedNumbers = sorted(numbers, reverse=True)
        trash = []
        straight = []
        for i in range(len(sortedNumbers)-1):
            if sortedNumbers[i+1] == sortedNumbers[i]:
                trash.append(i)
        trash = sorted(trash, reverse=True)
        for x in trash:
            sortedNumbers.pop(x)
        if sortedNumbers[-1] == 1:
            sortedNumbers.insert(0, 14)
        for i in range(len(sortedNumbers)-1):
            if sortedNumbers[i] - sortedNumbers[i+1] == 1:
                straight.append(sortedNumbers[i])
            else:
                straight = []
            if len(straight) == 4:
                straight.append(sortedNumbers[i+1])
                straight.sort()
                res = straight[4]
                return res + 59, straight
        return None

    def Flush(self, player):
        numbers = self.numberCheck(self.checkCards(player))
        power = self.powerCheck(self.checkCards(player))
        isColor = False
        for i in range(len(power)):
            sign = []
            signIndex = []
            nbInColor = []
            for y in range(len(power)):
                if power[i] == power[y] and i != y:
                    sign.append(power[y])
                    signIndex.append(y)
                    nbInColor.append(numbers[y])
                if len(sign) == 4:
                    nbInColor.append(numbers[i])
                    sign.append(power[i])
                    signIndex.append(i)
                    isColor = True
                    break
            if isColor:
                break
        nbInColor.sort()
        sign.sort()
        signIndex.sort()
        if len(sign) == 5:
            res = nbInColor[4]
            if nbInColor[0] == 1:
                res = 14
            return res + 72, nbInColor, sign[0]
        return None

    def straightFlush(self, player):
        Flushed = self.Flush(player)
        if Flushed:
            Straighted = self.Straight(player, Flushed[1])
            if Straighted:
                return Flushed[0] + 9, Straighted[1]
        return None

    def royalFlush(self, player):
        royale = self.straightFlush(player)
        if royale == 94:
            return 94, royale[1]
        return None

    def finalCheck(self, game):

        nbPlayer = game.Count()
        currentPlayer = game.currentPlayer()

        for _ in range(nbPlayer):
            print(currentPlayer.hand)
           # time.sleep(3)
            if self.royalFlush(currentPlayer):
                print(f"{currentPlayer.name}, Vous avez une Quinte Flush Royale !")
                currentPlayer.points += self.royalFlush(currentPlayer)[0]

            elif self.straightFlush(currentPlayer):
                # a voir
                print(
                    f"{currentPlayer.name}, Vous avez une Quinte Flush de {self.straightFlush(currentPlayer)[1]} !")
                currentPlayer.points += self.straightFlush(currentPlayer)[0]
            elif self.Quads(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez un carré de {self.Quads(currentPlayer)[1]} !")
                currentPlayer.points += self.Quads(currentPlayer)[0]

            elif self.Full(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez un full ! Brelan de {self.Full(currentPlayer)[1][0]} et Paire de {self.Full(currentPlayer)[1][1]} !")
                currentPlayer.points += self.Full(currentPlayer)[0]

            elif self.Flush(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez une couleur de {self.Flush(currentPlayer)[2]} !")
                currentPlayer.points += self.Flush(currentPlayer)[0]

            elif self.Straight(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez une suite ! Commençant par un {self.Straight(currentPlayer)[1][0]} et finissant par un {self.Straight(currentPlayer)[1][4]} !")
                currentPlayer.points += self.Straight(currentPlayer)[0]

            elif self.Trips(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez un Brelan de {self.Trips(currentPlayer)[1]} !")
                currentPlayer.points += self.Trips(currentPlayer)[0]

            elif self.twoPair(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez une Double Paire de {self.twoPair(currentPlayer)[1][0]} et de {self.twoPair(currentPlayer)[1][1]} !")
                currentPlayer.points += self.twoPair(currentPlayer)[0]

            elif self.Pair(currentPlayer):
                print(
                    f"{currentPlayer.name}, Vous avez une Paire de {self.Pair(currentPlayer)[1]} !")
                currentPlayer.points += self.Pair(currentPlayer)[0]

            else:
                print(
                    f"{currentPlayer.name}, malheurement vous n'avez pas de main...")
            print("\n\n")
            game.nextPlayer()
            currentPlayer = game.currentPlayer()

    def whoWon(self, game, totalMoney):
        nbPlayer = game.Count()
        currentPlayer = game.currentPlayer()
        multiWin = False
        nbPointWinner = 0
        equals = []

        for _ in range(nbPlayer):
            if currentPlayer.points > nbPointWinner:
                nbPointWinner = currentPlayer.points
                winner = currentPlayer
                equals = []
                equals.append(winner)
                multiWin = False
            elif currentPlayer.points == nbPointWinner:
                multiWin = True
                equals.append(currentPlayer)
            game.nextPlayer()
            currentPlayer = game.currentPlayer()
        if multiWin:
            winners = ""
            for x in equals:
                x.wallet += int(totalMoney / len(equals))
                winners += f"{x.name}, "
            print(f"{winners}vous avez tous gagné {int(totalMoney / len(equals))}€ !")
            self.resetPoints(game)
            return equals
        print(f"{winner.name}, tu as gagné {totalMoney}€ !")
        winner.wallet += totalMoney
        self.resetPoints(game)
        return winner

    def resetPoints(self, game):
        nbPlayer = game.Count()
        currentPlayer = game.currentPlayer()
        for _ in range(nbPlayer):
            currentPlayer.points = 0
            game.nextPlayer()
            currentPlayer = game.currentPlayer()

    def forfaitWinner(self, player, totalMoney):
        print(
            f"{player.name}, vos adversaire se sont couché, ce qui fait que vous remportez ma manche.")
        print(f"Vous gagnez {totalMoney}€")
        player.wallet += totalMoney
