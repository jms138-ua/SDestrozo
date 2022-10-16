import random
import AA_Registry

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
    MINE = "M"
    FOOD= "A"
    EMPTY = " "

    def __init__(self, column, row):
        self.row = row
        self.column = column

    def __str__(self):
        return "({x},{y})".format(x=self.getColumn(), y=self.getRow())

    def __eq__(self, other):
        return self.getColumn() == other.getColumn() and self.getRow() == other.getRow()

    def __add__(self, direc):
        return Cell(self.getColumn()+direc[0], self.getRow()+direc[1])

    def getColumn(self):
        return self.column

    def getRow(self):
        return self.row

    def normalize(self, columnsize, rowsize):
        self.row = self.getRow() % rowsize
        self.column = self.getColumn() % columnsize

class Map():
    SIZE = 20
    SIZE_CITY = SIZE/2
    RAND_ROW_VALUES_PERCENTAGE = [
        (Cell.EMPTY, 15),
        (Cell.MINE, 3),
        (Cell.FOOD, 2)
    ]

    def __init__(self):
        self.map = self.newRandMap()

    def __str__(self):
        strmap = ""
        for j, row in enumerate(self.map):
            strmap += "|"
            for i, value in enumerate(row):
                strmap += value
                strmap += "|"
            strmap += "\n"
        return strmap

    def getMap(self):
        return self.map

    def getCell(self, i, j):
        return self.map[j][i]

    def setCell(self, i, j, value):
        self.map[j][i] = value

    def newRandMap(self):
        map = []
        for _ in range(Map.SIZE):
            row = []
            for value, weight in Map.RAND_ROW_VALUES_PERCENTAGE:
                row.extend([value]*weight)
            random.shuffle(row)
            map.append(row)
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
        tocell.normalize(Map.SIZE, Map.SIZE)
        print(tocell)
        city = self.checkCity(fromcell, tocell)
        status = self.checkPosition(tocell)

        if status == Cell.EMPTY or status == Cell.FOOD or status == Cell.MINE:
            self.map.setCell(fromcell.getColumn(), fromcell.getRow(), Cell.EMPTY)
            if status == Cell.EMPTY:
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), alias)
            elif status == Cell.FOOD:
                # tu pokémon ha subido de nivel
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), alias)
            elif status == Cell.MINE:
                self.map.setCell(fromcell.getColumn(), tocell.getRow(), Cell.EMPTY)

        return status, tocell

    def checkPosition(self, cell):
        flag = False
        it = 0
        #comprobar qué hay en cada posición
        for i in range(Map.SIZE):
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

    def checkCity(self, fromcell, tocell):
        city = 0

        if tocell.getRow() <= Map.SIZE_CITY and tocell.getColumn() <= Map.SIZE_CITY:
            if fromcell.getRow() > Map.SIZE_CITY or fromcell.getColumn() > Map.SIZE_CITY:
                print("Cambio a ciudad 1")
                city = 1
        elif tocell.getRow() <= Map.SIZE_CITY and tocell.getColumn() > Map.SIZE_CITY:
            if fromcell.getRow() > Map.SIZE_CITY or fromcell.getColumn() <= Map.SIZE_CITY:
                print("Cambio a ciudad 2")
                city = 2
        elif tocell.getRow() > Map.SIZE_CITY and tocell.getColumn() <= Map.SIZE_CITY:
            if fromcell.getRow() <= Map.SIZE_CITY or fromcell.getColumn() > Map.SIZE_CITY:
                print("Cambio a ciudad 3")
                city = 3
        elif tocell.getRow() > Map.SIZE_CITY and tocell.getColumn() > Map.SIZE_CITY:
            if fromcell.getRow() <= Map.SIZE_CITY or fromcell.getColumn() <= Map.SIZE_CITY:
                print("Cambio a ciudad 4")
                city = 4
        # si city = 0 significa que no cambia de ciudad
        return city

#Local test
if __name__ == "__main__":
    game = Game()
    game.newPlayer("J", 4,19)
    print(game)
    game.move("J", Cell(4,19), Direction.S)
    print(game)

