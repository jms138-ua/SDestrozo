import random


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

    def __init__(self, c, r):
        self.column = c
        self.row = r

    def __str__(self):
        return "({x},{y})".format(x=self.getColumn(), y=self.getRow())

    def __eq__(self, other):
        return self.getColumn() == other.getColumn() and self.getRow() == other.getRow()

    def __add__(self, direc):
        return Cell(self.getColumn()+direc[0], self.getRow()+direc[1])

    def getColumn (self):
        return self.column

    def getRow (self):
        return self.row


class Map():
    SIZE = 20
    SIZE_CITY = SIZE/2

    def __init__(self):
        self.map = self.newRandMap()

    def __str__(self):
        strmap = ""
        for y in range(Map.SIZE):
            strmap += "|"
            for x in range(Map.SIZE):
                strmap += self.getCell(x,y)
                strmap += "|"
            strmap += "\n"
        return strmap

    def getSize():
        return Map.SIZE

    def getCell(self, x, y):
        return self.map[y][x]

    def setCell(self, x, y, value):
        self.map[y][x] = value

    def newRandMap(self):
        # TODO: El número de alimentos no debe ser divisible entre el número
        # de jugadores para evitar un empate, mucho menos número par
        bombs = food = players = value = zeroes =  0
        map = []
        count = 0

        for i in range(Map.getSize()):
            rowList = []
            for j in range(Map.getSize()):
                count = random.randrange(20) # de 0 a 19
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


class Game():
    def __init__(self):
        self.map = Map()

    def __str__(self):
        return str(self.map)

    def newPlayer(self, alias, x, y):
        self.map.setCell(x, y, alias)

    #def move(self, player, direc):
    def move(self, alias, fromcell, direc):
        tocell = fromcell + direc
        status = self.checkPosition(tocell)

        if status == Cell.NADA or status == Cell.ALIMENTO or status == Cell.MINA:
            self.map.setCell(fromcell.getColumn(), fromcell.getRow(), Cell.NADA)
            if status == Cell.NADA:
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), alias)
            elif status == Cell.ALIMENTO:
                # tu pokémon ha subido de nivel
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), alias)
            elif status == Cell.MINA:
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), Cell.NADA)

        return status, tocell

    def checkPosition(self, cell):
        flag = False
        it = 0
        #comprobar qué hay en cada posición
        for i in range(Map.getSize()):
            for row in self.map.map:
                if flag == True:
                    break
                it = it + 1
                if it > cell.getRow():
                    flag = True
                for ele in row:
                    status = row[cell.getColumn()]

        # print(cell.getRow()) # 4, viene de (4,2)
        print(status)
        return status

    def fight(self, player1, player2):
        pass

    def update(self, cell, status):
        pass


#Local test
if __name__ == "__main__":
    game = Game()
    game.newPlayer("J", 4,3)
    print(game)
    game.move("J", Cell(4,3), Direction.S)
    print(game)
