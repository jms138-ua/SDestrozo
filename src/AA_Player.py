import sys
import pygame
import tkinter
import math
import random
import tkinter.messagebox
import tkinter.filedialog
from pygame.locals import *
import time
from random import randrange
import AA_Engine, AA_Registry

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

pygame.init()
COLOR_INACTIVE = pygame.Color('white')
COLOR_ACTIVE = pygame.Color('yellow')
FONT = pygame.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.done = False
        self.textcopy = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.txt_surface = FONT.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.done = True
                    self.textcopy = self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen, login):
        if self.done == True and login == True:
            self.txt_surface = FONT.render('', True, 'black')
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            pygame.draw.rect(screen, 'black', self.rect, 2)
        else:
            # Blit the text.
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            # Blit the rect.
            pygame.draw.rect(screen, self.color, self.rect, 2)

def checkField(player, cell):
    if game.checkPosition(cell) == AA_Engine.Cell.MINE:
        screen.fill(RED)
        screen.blit(game_over, (200,330))

        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    elif game.checkPosition(cell) == AA_Engine.Cell.FOOD:
        player.setLevel(player.getLevel() + 1)
        print(player)

    elif game.checkPosition(cell) == AA_Engine.Cell.EMPTY:
        pass

    else:
        # value = game.fight(player, npc)
        value = 0

        if value > 0:
            print("has ganado")

        elif value < 0:
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
            elif game.map.getCell(fil, col) == AA_Engine.Cell.EMPTY:
                pygame.draw.rect(screen, WHITE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            elif game.map.getCell(fil, col) == AA_Engine.Cell.FOOD:
                pygame.draw.rect(screen, GREEN, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
            else:
                pygame.draw.rect(screen, BLUE, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)

if __name__=="__main__":

    root=tkinter.Tk()
    root.withdraw()

    x = random.randint(0, 19)
    y = random.randint(0, 19)

    game = AA_Engine.Game()
    player = None
    fromcell = AA_Engine.Cell(x,y)
    
    # npc de prueba para testear el fight, falta una interacción
    # npc = game.newPlayer("NPC", AA_Engine.Cell(4, 4))
    # npc.setLevel(10)

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

    active = False
    text = ''
    font2 = pygame.font.Font(None, 32)
    user = ''
    passwd = ''

    text_input_box1 = InputBox(0, 700, width/2 - 100, 32, "Usuario")
    text_input_box2 = InputBox(0, 733, width/2 - 100, 32, "Contraseña")
    input_boxes = [text_input_box1, text_input_box2]

    running=True
    start = False
    login = False
    created = False

    while running:

        if login == False:

            fuente= pygame.font.Font(None, 30)
            texto= fuente.render("", True, BLACK)
            screen.blit(texto, [width-120, AA_Engine.Map.SIZE*(TAM+MARGEN)+MARGEN+15])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for box in input_boxes:
                    box.handle_event(event)

            if input_boxes[0].done == True:
                user = input_boxes[0].textcopy
            if input_boxes[1].done == True:
                passwd = input_boxes[1].textcopy
        
            # !!! CREAR PRIMERO EL USUARIO DESDE AA_Registry.create_user o no va
            if user != '' and passwd != '':
                AA_Registry.create_db()
                # create user if not exists? puede ser buena idea
                # AA_Registry.create_user_db(user,passwd)
                res = AA_Registry.select_user_db(user, passwd)

                if (res != None):
                    login = True

            for box in input_boxes:
                box.update()
                box.draw(screen, login)
            
        if login == True:
            texto= fuente.render("Nivel: "+str(player.getLevel()), True, YELLOW)
            screen.blit(texto, [width-120, AA_Engine.Map.SIZE*(TAM+MARGEN)+MARGEN+15])

        if created == False:
            player = game.newPlayer(input_boxes[0].textcopy, AA_Engine.Cell(x, y))
            created = True

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    checkField(player, fromcell + AA_Engine.Direction.N)
                    game.move(player.getAlias(), fromcell, AA_Engine.Direction.N)
                    fromcell = fromcell + AA_Engine.Direction.N
                elif event.key == pygame.K_RIGHT:
                    checkField(player, fromcell + AA_Engine.Direction.S)
                    game.move(player.getAlias(), fromcell, AA_Engine.Direction.S)
                    fromcell = fromcell + AA_Engine.Direction.S
                elif event.key == pygame.K_UP:
                    checkField(player, fromcell + AA_Engine.Direction.W)
                    game.move(player.getAlias(), fromcell, AA_Engine.Direction.W)
                    fromcell = fromcell + AA_Engine.Direction.W
                elif event.key == pygame.K_DOWN:
                    checkField(player, fromcell + AA_Engine.Direction.E)
                    game.move(player.getAlias(), fromcell, AA_Engine.Direction.E)
                    fromcell = fromcell + AA_Engine.Direction.E
                fromcell.normalize(game.map.SIZE, game.map.SIZE)

        pygame.display.flip()

        clock.tick(40)

        printMap(game)

    pygame.quit()
    sys.exit()
