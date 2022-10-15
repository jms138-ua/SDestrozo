'''
- ARGS:
    - Puerto de escucha
    - Maximo numero de jugadores
    - Puerto AA_Weather
- RETURNS:
    - Tablero
- DO:
    - 4 peticiones a AA_Weather
'''

from random import randrange

SIZE_MAP = 20
SIZE_CITY = SIZE_MAP / 2

class Direction():
    N = (0,-1)
    S = (0,1)
    W = (-1,0)
    E = (1,0)
    NW = (-1,-1)
    NE = (1,-1)
    SW = (-1,1)
    SE = (1,1)

class Cell():
    JUGADOR = "J"
    MINA = "M"
    ALIMENTO = "A"
    NADA = " "

    def __init__(self, r, c):
        self.row = r
        self.column = c

    def __str__(self):
        return "(" + str(self.getRow()) + ", " + str(self.getColumn()) + ")"

    def __eq__(self, other):
        return self.getColumn() == other.getColumn() and self.getRow() == other.getRow()

    def __add__(self, direc):
        return Cell(self.getRow()+direc[0], self.getColumn()+direc[1])

    def getRow (self):
        return self.row

    def getColumn (self):
        return self.column


class Map():
    def __init__(self):
        self.map = self.newMap()
        self.height = self.width = SIZE_MAP

    def __str__(self):
        strmap = ""
        for i in range(SIZE_MAP):
            strmap += str(self.map[i])
            strmap += "\n"
        return strmap

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getCell(self, x, y):
        return self.map[y][x]

    def setCell(self, x, y, value):
        self.map[y][x] = value

    def newMap(self):
        # TODO: El número de alimentos no debe ser divisible entre el número
        # de jugadores para evitar un empate, mucho menos número par
        bombs = food = players = value = zeroes =  0
        map = []
        count = 0

        for i in range(SIZE_MAP):
            rowList = []
            for j in range(SIZE_MAP):
                count = randrange(20) # de 0 a 19
                #count = count + 1
                if count < 8:
                    bombs = bombs + 1
                    value = Cell.MINA
                elif count >= 8 and count <= 10:
                    food = food + 1
                    value = Cell.ALIMENTO
                elif count > 10:
                    value = Cell.NADA

                #rowList.append(count)
                rowList.append(value)
            map.append(rowList)
        return map

    def newPlayer(self, x, y):
        self.setCell(x, y, Cell.JUGADOR)

    def checkCell(self, cell):
        flag = False
        it = 0
        #comprobar qué hay en cada posición
        for i in range(SIZE_MAP):
            for row in self.map:
                if flag == True:
                    break
                it = it + 1
                if it > cell.getColumn():
                    flag = True
                for ele in row:
                    status = row[cell.getRow()]

        # print(cell.getRow()) # 4, viene de (4,2)
        print(status)
        return status

    def move(self, fromcell, direc):
        tocell = fromcell + direc
        status = self.checkCell(tocell)
        # si es nada solo se mueve, si es alimento se mueve y sube nivel
        # si es mina se mueve y desparece la mina y el jugador
        self.setCell(fromcell.getRow(), fromcell.getColumn(), Cell.NADA)
        self.setCell(tocell.getRow(), tocell.getColumn(), Cell.JUGADOR)

        return status, tocell

    def fight(player1, player2):
        pass


if __name__=="__main__":
    map = Map()
    map.newPlayer(4,3)
    print(map)
    map.move(Cell(4,3), Direction.NW)
    print(map)
