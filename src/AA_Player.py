import sys
import pygame
import tkinter
import math
import tkinter.messagebox
import tkinter.filedialog
from pygame.locals import *
import time
from random import randrange
import AA_Engine

SIZE_MAP = 20
SIZE_CITY = SIZE_MAP / 2

MARGEN = 5
MARGEN_SUPERIOR = 60
MARGEN_INFERIOR = 60
TAM = 30

BLACK=(0,0,0)
WHITE=(255, 255,255)
GREEN=(0, 255,0)
RED=(255, 0, 0)
BLUE=(0, 0, 255)
YELLOW=(255, 255, 0)

def printMap(map):

    screen.fill(BLACK)
    for fil in range(game.map.SIZE):
        for col in range(game.map.SIZE):
            if game.map.getCell(fil, col) == "M":
                pygame.draw.rect(screen, RED, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if game.map.getCell(fil, col) == " ":
                pygame.draw.rect(screen, WHITE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if game.map.getCell(fil, col) == "A":
                pygame.draw.rect(screen, GREEN, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            # El jugador de prueba
            if game.map.getCell(fil, col) == "J":
                pygame.draw.rect(screen, BLUE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

if __name__=="__main__":
    game = AA_Engine.Game()
    game.newPlayer("J", 4,19)
    fromcell = AA_Engine.Cell(4,19)
    pygame.init()
    clock = pygame.time.Clock()

    width = game.map.SIZE*(TAM+MARGEN) + MARGEN
    height = MARGEN_INFERIOR + game.map.SIZE*(TAM+MARGEN) + MARGEN
    dimension = [width, height]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("SDestrozo")

    running= True

    while running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move("J", fromcell, AA_Engine.Direction.N)
                    fromcell = fromcell + AA_Engine.Direction.N
                if event.key == pygame.K_RIGHT:
                    game.move("J", fromcell, AA_Engine.Direction.S)
                    fromcell = fromcell + AA_Engine.Direction.S
                if event.key == pygame.K_UP:
                    game.move("J", fromcell, AA_Engine.Direction.W)
                    fromcell = fromcell + AA_Engine.Direction.W
                if event.key == pygame.K_DOWN:
                    game.move("J", fromcell, AA_Engine.Direction.E)
                    fromcell = fromcell + AA_Engine.Direction.E
                fromcell.normalize(game.map.SIZE, game.map.SIZE)
            if event.type == pygame.QUIT:
                running = False

        clock.tick(40)

        printMap(game)

    pygame.quit()
    sys.exit()
