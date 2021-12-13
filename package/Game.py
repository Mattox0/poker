from .Players import Player


class wholeGame:
    def __init__(self):
        self.players = []
        self.indexPlayer = 0
        self.foldedPlayers = []
        self.deadPlayers = []

    def Count(self):
        return len(self.players)

    def initGame(self):
        nbPlayers = 1
        players = []
        while nbPlayers < 2 or nbPlayers > 4:
            nbPlayers = input("Combien de joueurs ? (entre 2 et 4) : ")
            try:
                nbPlayers = int(nbPlayers)
            except ValueError:
                print("Vous n'avez pas entré de nombre.\nRéessayez !")
                nbPlayers = 1
                continue
            if nbPlayers < 2 or nbPlayers > 4:
                print("Nombre de joueurs invalide\nRéessayez !")

        for a in range(nbPlayers):
            players += [Player(input(f"Nom du joueur {a+1}: "))]
        self.players = players
        return nbPlayers

    def currentPlayer(self):
        self.indexPlayer = self.indexPlayer % len(self.players)
        return self.players[self.indexPlayer]

    def nextPlayer(self):
        self.indexPlayer = self.players.index(self.getNextPlayer())

    def getNextPlayer(self):
        return self.players[(self.indexPlayer + 1) % len(self.players)]

    def checkAllIn(self):
        compt = 0
        for _ in range(self.Count()):
            player = self.currentPlayer()
            if player.allIn == True:
                compt += 1
            self.nextPlayer()
        if compt == (self.Count() - 1):
            return True
        return False

    def promptCards(self, player):
        validAns = False
        while validAns == False:
            confirm = input(
                player.name + ", Voulez vous voir vos cartes? (oui/non)")
            if confirm == "yes" or confirm == "oui" or confirm == "o" or confirm == "y" or confirm == "Y":
                player.showCards(1)
                validAns = True
            elif confirm == "no" or confirm == "non" or confirm == "n" or confirm == "N":
                print("Vous n'avez pas voulu voir vos cartes.")
                validAns = True
            else:
                print(
                    "Erreur, vous n'avez pas saisi \"oui\" ou \"non\". Veuillez réessayer")

    def foldPlayer(self, player):
        toPop = self.players.index(player)
        self.foldedPlayers.append(player)
        self.players.pop(toPop)

    def sleepingPlayers(self):
        return self.foldedPlayers

    def wakeUp(self, player):
        player.status = True
        self.foldedPlayers.insert(0, self.foldedPlayers.pop(
            self.foldedPlayers.index(player)))
        self.players.append(player)
        self.foldedPlayers.pop(0)

    def Kill(self, player):
        self.deadPlayers.append(player)
        self.players.pop(self.players.index(player))

    def checkFoldedPlayers(self):
        if self.Count() == 1:
            return True
        return False
