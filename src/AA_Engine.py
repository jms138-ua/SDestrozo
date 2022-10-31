"""
client.send_obj(("user","password"))
client.recv_msg() -> MSGOPRE
client.send_msg("Ready")
client.with_kafka.recv() -> "None": Initial Map
thread1:
    while movement:
        client.with_kafka.send("alias":"direction")
thread2:
    while any player movement:
        client.with_kafka.recv() -> "alias": Map
"""

from common_utils import socket, MySocket, rundb

from kafka import KafkaConsumer, KafkaProducer
import sys, threading, pickle, random


ADDR = ("", int(sys.argv[1]))
ADDR__AA_WEATHER = ("localhost", int(sys.argv[3]))

FDATA_DB = "../data/db.db"

MAX_PLAYERS = int(sys.argv[2])

MSGREJOIN = "Usuario unido a la partida"
MSGERRJOIN_NOT_EXISTS = "Error. La cuenta no coincide con ninguna registrada"
MSGERRJOIN_ALREADY_JOINED = "Error. Usuario ya unido a la partida"
MSGERRJOIN_MAX_PLAYERS = "Error. Maximo de usuarios permitidos en la partida"


class Requests():

    @staticmethod
    def get_cities(n):
        cities = set()
        while(len(cities) < 4):
            with MySocket("TCP", ADDR__AA_WEATHER) as client:
                city = client.recv_obj()
                if city["city"] not in cities:
                    cities.add(city["city"])
                    yield city


class Player():
    def __init__(self, alias, password):
        self.alias = alias
        self.password = password
        self.pos = Cell(-1, -1)
        self.ef = random.randint(-10,10)
        self.ec = random.randint(-10,10)
        self.__level = 1
        self.temperature = None

    def __str__(self):
        return "Usuario " + self.alias + ", con nivel " + str(self.getTotalLevel())

    def isAlive(self):
        return self.__level != -1

    def die(self):
        self.__level = -1

    def upLevel(self):
        self.__level += 1

    def getTotalLevel(self):
        if self.temperature is None:
            return self.__level
        elif self.temperature <= 10:
            return self.__level + self.ef
        elif self.temperature >= 25:
            return self.__level + self.ec
        else:
            return self.__level


class Direction():
    N = (0,-1)
    S = (0,1)
    W = (-1,0)
    E = (1,0)
    NW = (-1,-1)
    NE = (1,-1)
    SW = (-1,1)
    SE = (1,1)

    def fromStr(text):
        return vars(Direction)[text]


class Cell():
    MINE = "M"
    FOOD= "A"
    EMPTY = " "

    NOTPLAYER = (MINE, FOOD, EMPTY)

    def __init__(self, column, row):
        self.row = row
        self.column = column

    def __str__(self):
        return "({i},{j})".format(i=self.column, j=self.row)

    def __eq__(self, other):
        return self.column == other.getColumn() and self.row == other.getRow()

    def __add__(self, direcc):
        return Cell(self.column+direcc[0], self.row+direcc[1])

    def getColumn(self):
        return self.column

    def getRow(self):
        return self.row

    def normalize(self, columnsize, rowsize):
        self.row %= rowsize
        self.column %= columnsize


class Map():
    SIZE = 20
    SIZE_CITY = SIZE/2
    RAND_ROW_VALUES_PERCENTAGE = [
        (Cell.EMPTY, 15),
        (Cell.MINE, 3),
        (Cell.FOOD, 2)
    ]

    def __init__(self):
        self.map = Map.newRandMap()

    def __str__(self):
        strmap = ""
        for j, row in enumerate(self.map):
            strmap += "|"
            for i, value in enumerate(row):
                strmap += str(value)
                strmap += "|"
            strmap += "\n"
        return strmap

    def getMap(self):
        return self.map

    def getCell(self, cell):
        return self.map[cell.getRow()-1][cell.getColumn()-1]

    def setCell(self, cell, value):
        self.map[cell.getRow()-1][cell.getColumn()-1] = value

    def setValueCell(self, cell, value):
        if self.getCell(cell) in Cell.NOTPLAYER:
            self.setCell(cell, [value,])
        else:
            self.map[cell.getRow()-1][cell.getColumn()-1].append(value)

    def delValueCell(self, cell, value):
        self.map[cell.getRow()-1][cell.getColumn()-1].remove(value)

    def newRandMap():
        map = []
        for _ in range(Map.SIZE):
            row = []
            for value, weight in Map.RAND_ROW_VALUES_PERCENTAGE:
                row.extend([value]*weight)
            random.shuffle(row)
            map.append(row)
        return map

    def getCity(cities, cell):
        '''
        |0|1|
        |2|3|
        '''
        if cell.getColumn() < Map.SIZE_CITY:
            if cell.getRow() < Map.SIZE_CITY:
                return cities[0]
            else:
                return cities[1]
        else:
            if cell.getRow() < Map.SIZE_CITY:
                return cities[2]
            else:
                return cities[3]


class Game():
    def __init__(self):
        self.map = Map()
        self.cities = list(Requests.get_cities(4))
        self.players = dict()

    def __str__(self):
        strgame = str(self.map)
        for player in self.players.values():
            strgame += str(player) + "\n"
        return strgame

    def getMap(self):
        return self.map.getMap()

    def getPlayers(self):
        return self.players

    def isended(self):
        return len(self.players) == 1

    def updatePlayer(self, player, pos):
        player.pos = pos
        player.temperature = Map.getCity(self.cities, pos)["temperature"]

    def newRandPlayer(self, player):
        while True:
            i = random.randint(1,Map.SIZE)
            j = random.randint(1,Map.SIZE)
            pos = Cell(i,j)

            if self.map.getCell(pos) == Cell.EMPTY:
                self.updatePlayer(player, pos)
                self.players[player.alias] = player
                self.map.setValueCell(pos, player.alias)
                break

    def move(self, playeralias, direcc):
        player = self.players[playeralias]
        topos = (player.pos + direcc)
        topos.normalize(Map.SIZE,Map.SIZE)
        self.update(player, topos)

    def update(self, player, topos):
        self.map.setCell(player.pos, Cell.EMPTY)
        self.updatePlayer(player, topos)

        value = self.map.getCell(topos)
        if value == Cell.EMPTY:
            self.map.setValueCell(topos, player.alias)
        elif value == Cell.FOOD:
            self.map.setValueCell(topos, player.alias)
            player.upLevel()
        elif value == Cell.MINE:
            self.map.setCell(topos, Cell.EMPTY)
            self.players.pop(player.alias)
            player.die()
        else:
            self.map.setValueCell(topos, player.alias)
            self.fight(player)

    def fight(self, player1):
        for player2 in self.players.values():
            if player2.pos == player.pos and player.getTotalLevel() != player2.getTotalLevel():
                playertodel = max(player1, player2, key=lambda player: player.getTotalLevel())
                self.map.delValueCell(playertodel.pos, playertodel.alias)
                self.players.pop(playertodel.alias)
                playertodel.die()

#==================================================

def print_count(text, textargs, nreverselines):
    if nreverselines == -1:
        sys.stdout.write(text.format(*textargs))
        sys.stdout.write("\n")
    else:
        sys.stdout.write("\033[{n}A".format(n=nreverselines+1))
        sys.stdout.write(text.format(*textargs))
        sys.stdout.write("\033[{n}B".format(n=nreverselines+1))
        sys.stdout.write("\033[0G")
    sys.stdout.flush()

class ConnPlayer(Player):
    def __init__(self, conn, alias, password):
        self.conn = conn
        self.ready = False
        super().__init__(alias, password)

    def is_user_correct_login_db(player):
        res = rundb(FDATA_DB,
            """
            SELECT password
            FROM players
            WHERE alias = ?
            """
            ,(player.alias,)
        )
        user_fetch = res.fetchone()
        return user_fetch is not None and user_fetch[0] == player.password

PRINT_USERS_JOIN = "Usuarios unidos: {0}/{1}"
PRINT_USERS_READY = "Usuarios listos: {0}/{1}"

def handle_player_join(conn, direcc, server, players):
    player = ConnPlayer(conn, *server.recv_obj())

    if not ConnPlayer.is_user_correct_login_db(player):
        server.send_msg(MSGERRJOIN_NOT_EXISTS)
        conn.close()
        return

    if any(map(lambda p: p.alias == player.alias, players)):
        server.send_msg(MSGERRJOIN_ALREADY_JOINED)
        conn.close()
        return

    """
    Two players can join at the same time,
    and the first reaches the MAX_PLAYERS
    with an exception in the second.

    Is discarded by almost null probability
    and does not affect the system
    (can be controlled in the user)
    """
    if len(players) == MAX_PLAYERS:
        server.send_msg(MSGERRJOIN_MAX_PLAYERS)
        conn.close()
        return

    players.add(player)
    server.send_msg(MSGREJOIN)
    print_count(PRINT_USERS_JOIN, (len(players), MAX_PLAYERS), 1)
    users_ready = {p for p in players if p.ready}
    print_count(PRINT_USERS_READY, (len(users_ready), len(players)), 0)

    server.recv_msg()   #Ready
    player.ready = True
    users_ready = {p for p in players if p.ready}
    print_count(PRINT_USERS_READY, (len(users_ready), len(players)), 0)

    if len(users_ready) == len(players) >= 2:
        server.close()

#==================================================

def start_game(players):
    game = Game()

    for player in players:
        game.newRandPlayer(player)

    print("Empieza el juego!\n")
    print(game)

    producer = KafkaProducer(
        bootstrap_servers=["localhost:29092"],
        value_serializer=lambda v: pickle.dumps(v)
    )

    consumer = KafkaConsumer(
        "movement",
        group_id = "engine",
        bootstrap_servers = ["localhost:29092"],
        auto_offset_reset = "earliest",
        enable_auto_commit = True,
        value_deserializer = lambda v: pickle.loads(v)
    )

    producer.send("map", value={"None":game.getMap()})

    for msg in consumer:
        playeralias, direcc = msg.value.items()
        game.move(playeralias, Direction.fromStr(direcc))
        producer.send("map", value={playeralias:game.getMap()})

        if game.isended():
            print("La partida ha terminado")
            print("Ha ganado el jugador", game.getPlayers()[0])
            break

#==================================================

while True:
    if input("Crear partida? (s/): ") not in ("s","S","y","Y"):
        continue

    print("Esperando jugadores...")

    with MySocket("TCP", ADDR) as server:
        server.settimeout(0.1)  #Any time

        print_count(PRINT_USERS_JOIN, (0, MAX_PLAYERS), -1)
        print_count(PRINT_USERS_READY, (0, 0), -1)
        players = set()

        while True:
            try:
                conn, direcc = server.accept()
                threading.Thread(
                    target=handle_player_join,
                    args=(conn, direcc, server, players),
                    name=direcc[0],
                    daemon=True
                ).start()
            except socket.timeout:
                """
                Linux fun:
                accept(), if is running, not gives an error if the server is closed
                settimeout and handle the exception to repeat the accept()
                """
                continue
            except socket.error:
                """
                Last player to accept closes the server
                accept() that was waiting gives an error
                """
                break

        start_game(players)