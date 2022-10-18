'''
- ARGS:
    - Puerto de escucha
- RETURNS:
    - Nada
- DO:
    - Guardar jugadores en un archivo
'''
import sys, csv, random, sqlite3
import AA_Engine

# ADDR = ("", int(sys.argv[2]))

FDATA_PLAYERS = "./data/db.db"

def save_players(players):
    with open(FDATA_PLAYERS, 'w') as f:
        file = csv.writer(f)
        file.writerow(players)

def create_database():
    con = sqlite3.connect(FDATA_PLAYERS)
    cur = con.cursor()
    cur.execute("CREATE TABLE players(alias, password)")

def create_user(alias, password):
    con = sqlite3.connect(FDATA_PLAYERS)
    cur = con.cursor()
    #cur.execute("INSERT INTO players VALUES('"+alias+"', '"+password"+')")
    cur.execute("INSERT INTO players VALUES('{alias}', '{passwd}')".format(alias=alias, passwd=password))
    con.commit()
    res = cur.execute("SELECT alias FROM players")
    print(res.fetchall())

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
    cell = AA_Engine.Cell(-1,-1)
    name = str(input("¿Cómo te llamas? "))
    password = str(input("¿Cúal es tu contraseña? "))
    create_database()
    player = Player(name, password, 1, random.randint(-10, 10), random.randint(-10, 10), cell)

    create_user(name, password)
