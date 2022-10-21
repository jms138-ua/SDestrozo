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

def checkField(cell):
    if game.checkPosition(cell) == AA_Engine.Cell.MINE:
        screen.fill(RED)
        screen.blit(game_over, (200,330))
           
        pygame.display.update() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
    '''
    if game.checkPosition(cell) == AA_Engine.Cell.FOOD:
        screen.fill(GREEN)
        screen.blit(you_win, (230,330))
           
        pygame.display.update() 
        time.sleep(2)
        pygame.quit()
        sys.exit()
    '''

def printMap(map):

    screen.fill(BLACK)
    for fil in range(game.map.SIZE):
        for col in range(game.map.SIZE):
            if game.map.getCell(fil, col) == AA_Engine.Cell.MINE:
                pygame.draw.rect(screen, RED, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if game.map.getCell(fil, col) == AA_Engine.Cell.EMPTY:
                pygame.draw.rect(screen, WHITE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            if game.map.getCell(fil, col) == AA_Engine.Cell.FOOD:
                pygame.draw.rect(screen, GREEN, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            # El jugador de prueba
            if game.map.getCell(fil, col) == "J":
                pygame.draw.rect(screen, BLUE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

if __name__=="__main__":
    game = AA_Engine.Game()
    game.newPlayer("J", 4,19)
    fromcell = AA_Engine.Cell(4,19)
    pygame.init()
    
    font = pygame.font.SysFont("Verdana", 60)
    game_over = font.render("Game Over", True, BLACK)
    you_win = font.render("You Win", True, BLACK)
    
    clock = pygame.time.Clock()

    width = game.map.SIZE*(TAM+MARGEN) + MARGEN
    height = MARGEN_INFERIOR + game.map.SIZE*(TAM+MARGEN) + MARGEN
    dimension = [width, height]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("SDestrozo")

    running=True

    while running:
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    checkField(fromcell + AA_Engine.Direction.N)
                    game.move("J", fromcell, AA_Engine.Direction.N)
                    fromcell = fromcell + AA_Engine.Direction.N
                if event.key == pygame.K_RIGHT:
                    checkField(fromcell + AA_Engine.Direction.S)
                    game.move("J", fromcell, AA_Engine.Direction.S)
                    fromcell = fromcell + AA_Engine.Direction.S
                if event.key == pygame.K_UP:
                    checkField(fromcell + AA_Engine.Direction.W)
                    game.move("J", fromcell, AA_Engine.Direction.W)
                    fromcell = fromcell + AA_Engine.Direction.W
                if event.key == pygame.K_DOWN:
                    checkField(fromcell + AA_Engine.Direction.E)
                    game.move("J", fromcell, AA_Engine.Direction.E)
                    fromcell = fromcell + AA_Engine.Direction.E
                fromcell.normalize(game.map.SIZE, game.map.SIZE)
            if event.type == pygame.QUIT:
                running = False

        clock.tick(40)

        printMap(game)

    pygame.quit()
    sys.exit()
