'''
- ARGS:
    - Puerto de escucha
- RETURNS:
    - Nada
- DO:
    - Guardar jugadores en un archivo
'''
import sys, csv

# ADDR = ("", int(sys.argv[2]))

FDATA_PLAYERS = "./data/players.csv"

def save_players(players):
    with open(FDATA_PLAYERS, 'w') as f:
        file = csv.writer(f)
        file.writerow(players)

class Player():

    def __init__(self, a, p, l, ef, ec):
        self.alias = a
        self.password = p
        self.level = l
        self.ef = ef
        self.ec = ec

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

if __name__=="__main__":
    players = []
    name = str(input("¿Cómo te llamas? "))
    password = str(input("¿Cúal es tu contraseña? "))
    player = Player(name, password, 1, 0, 0)
    players.append(player)
    #print(player)

    save_players(players)
