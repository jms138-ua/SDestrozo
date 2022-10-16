'''
- ARGS:
    - Puerto de escucha
- RETURNS:
    - Nada
- DO:
    - Guardar jugadores en un archivo
'''
import sys, csv
import AA_Engine

# ADDR = ("", int(sys.argv[2]))

FDATA_PLAYERS = "./data/players.csv"

def save_players(players):
    with open(FDATA_PLAYERS, 'w') as f:
        file = csv.writer(f)
        file.writerow(players)

class Player():

    def __init__(self, a, p, l, ef, ec, cell):
        self.alias = a
        self.password = p
        self.level = l
        self.ef = ef
        self.ec = ec
        self.cell = cell

    def __str__(self):
        return self.getAlias() + ";" + self.getPassword()

    def getAlias (self):
        return self.alias

    def getPassword (self):
        return self.password

    def getLevel (self):
        return self.level

    def setLevel (self, l):
        self.level = l

    def getCell (self):
        return self.cell

    def setCell (self, cell):
        self.cell = cell

if __name__=="__main__":
    players = []
    cell = AA_Engine.Cell(-1,-1)
    name = str(input("¿Cómo te llamas? "))
    password = str(input("¿Cúal es tu contraseña? "))
    player = Player(name, password, 1, 0, 0, cell)
    players.append(player)

    save_players(players)
