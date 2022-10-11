import sys, pygame
import tkinter
import math
import tkinter.messagebox
import tkinter.filedialog
from pygame.locals import *
import time
from random import randrange

SIZE_MAP = 20
SIZE_CITY = SIZE_MAP / 2

MARGEN = 5
MARGEN_INFERIOR = 60
TAM = 30

BLACK=(0,0,0)
WHITE=(255, 255,255)
GREEN=(0, 255,0)
RED=(255, 0, 0)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)

class Cell():
    def __init__(self, r, c):
        self.row = r
        self.column = c
        
    def getRow (self):
        return self.row
    
    def getColumn (self):
        return self.column
    
    def __eq__(self, other):
        return self.getColumn() == other.getColumn() and self.getRow() == othergetRow()

class Map():
    def __init__(self):        
        self.map = setMap()
        self.height = SIZE_MAP
        self.width = SIZE_MAP
        
    def getHeight (self):
        return self.height
    
    def getWidth (self):
        return self.width
        
    def getCell(self, y, x):
        return self.map[y][x]
    
    def setCell(self, y, x, value):
        self.map[y][x] = value
        
def setMap():
    
    # TODO: El número de alimentos no debe ser divisible entre el número
    # de jugadores para evitar un empate, mucho menos número par
    map = []
    bombs = 0
    food = 0
    players = 0
    value = 0
    zeroes = 0
    
    for i in range(SIZE_MAP):
        rowList = []
        for j in range(SIZE_MAP):
            count = randrange(20) # de 0 a 19
            if count == 0:
                zeroes = zeroes + 1
            if count == 0 and players == 0 and zeroes >= 10:
                players = players + 1
                value = 3
            elif count < 8:
                bombs = bombs + 1
                value = 0
            elif count >= 8 and count <= 10:
                food = food + 1
                value = 2
            elif count > 10:
                value = 1
            
            rowList.append(value)
        map.append(rowList)

    return map

def printMap(map):
    
    screen.fill(BLACK)
    for fil in range(map.getHeight()):
        for col in range(map.getWidth()):
            if map.getCell(fil, col) == 0:
                pygame.draw.rect(screen, RED, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if map.getCell(fil, col) == 1:
                pygame.draw.rect(screen, WHITE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if map.getCell(fil, col) == 2:
                pygame.draw.rect(screen, GREEN, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            # El jugador de prueba
            if map.getCell(fil, col) == 3:
                pygame.draw.rect(screen, BLUE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
        
if __name__=="__main__":
    map = Map()
    pygame.init()
    clock = pygame.time.Clock()
    
    width = map.getWidth()*(TAM+MARGEN) + MARGEN
    height = MARGEN_INFERIOR + map.getHeight()*(TAM+MARGEN) + MARGEN
    dimension = [width, height]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("SDestrozo")
    
    running= True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               
                running = False
        
        printMap(map)
        
        pygame.display.flip()
        clock.tick(40)
    
    pygame.quit()
    