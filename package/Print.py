

def startGame():
    print("""
	o--------------------o
	| DEBUT DE LA PARTIE |
	o--------------------o
	""")


def nbRound(n):
    print(f"""\n
    o------------o
    | MANCHE {n}   |
    o------------o
    """)


def roundPlayer(joueur):
    phrase = ""
    phrase += "| " + joueur.name + ", c'est à vous !" + \
        int(27-len(joueur.name))*' ' + "|"
    print(f'''
    o--------------------------------------------o
    {phrase}
    o--------------------------------------------o''')


def endOfRound():
    print('''
   o-----------------------------------o
   | FIN DE MANCHE -- VERIF DES CARTES |
   o-----------------------------------o
    ''')


def printFlop():
    print('''
	o-----------------------------------o
	|               FLOP                |
	o-----------------------------------o
	''')


def printTurn():
    print('''
	o-----------------------------------o
	|               TURN                |
	o-----------------------------------o
	''')


def printRiver():
    print('''
	o-----------------------------------o
	|               RIVER               |
	o-----------------------------------o
	''')


def printEmptyTable():
    print('''
	o-----------------------------------o
	|  La table est actuellement vide   |
	o-----------------------------------o
	''')


def printTableFlop(cardsOnTable):
    print(f'''
    o-----------------------------------------------------------------o
    | La table actuelle est: {cardsOnTable[0]} {cardsOnTable[1]} {cardsOnTable[2]} |
    o-----------------------------------------------------------------o
    ''')


def printTableTurn(cardsOnTable):
    print(f'''
    o------------------------------------------------------------------------------o
    | La table actuelle est: {cardsOnTable[0]} {cardsOnTable[1]} {cardsOnTable[2]} {cardsOnTable[3]} |
    o------------------------------------------------------------------------------o
    ''')


def printTableRiver(cardsOnTable):
    print(f'''
    o-------------------------------------------------------------------------------------------o
    | La table actuelle est: {cardsOnTable[0]} {cardsOnTable[1]} {cardsOnTable[2]} {cardsOnTable[3]} {cardsOnTable[4]} |
    o-------------------------------------------------------------------------------------------o
    ''')
