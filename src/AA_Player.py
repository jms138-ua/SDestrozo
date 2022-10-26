import sys
import pygame
import math
import random
from pygame.locals import *
import time
from random import randrange
import AA_Engine
from common_utils import MySocket

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

ADDR = ("localhost", int(sys.argv[1])) # de registry

# puerto engine: 1234
# weather 9999
# registry: 5000

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
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.txt_surface = FONT.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
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

def landingPage():

    running = True
    option = 0
    screen.fill(BLACK)

    # width x height = 705 x 765
    # bg = pygame.image.load("descargar.jpg")
    # screen.blit(bg, (0, 0))

    # x, y, w, h
    rect1 = pygame.Rect(280, 100, 170, 32)
    txt_surface = FONT.render(' Crear usuario', True, 'white')
    screen.blit(txt_surface, (280+5, 100+5))
    pygame.draw.rect(screen, 'yellow', rect1, 2)

    rect2 = pygame.Rect(280, 250, 170, 32)
    txt_surface = FONT.render('   Editar perfil', True, 'white')
    screen.blit(txt_surface, (280+5, 250+5))
    pygame.draw.rect(screen, 'yellow', rect2, 2)

    rect3 = pygame.Rect(280, 400, 170, 32)
    txt_surface = FONT.render('  Borrar perfil', True, 'white')
    screen.blit(txt_surface, (280+5, 400+5))
    pygame.draw.rect(screen, 'yellow', rect3, 2)

    rect4 = pygame.Rect(280, 550, 170, 32)
    txt_surface = FONT.render(' Iniciar partida', True, 'white')
    screen.blit(txt_surface, (280+5, 550+5))
    pygame.draw.rect(screen, 'yellow', rect4, 2)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                option = 1
            elif rect2.collidepoint(event.pos):
                option = 2
            elif rect3.collidepoint(event.pos):
                option = 3
            elif rect4.collidepoint(event.pos):
                option = 4

    pygame.display.flip()

    # login, crear usuario, editar perfil (actualizar y borrar)

    # para hoy: pantalla registro y conexión
    # mañana: conexión registro
    # miércoles: conexión engine (login), interfaz ya bien, conexión engine con mapa

    return running, option

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

    text_input_boxa1 = InputBox(250, 150, width/2 - 100, 32, "")
    text_input_boxa2 = InputBox(250, 350, width/2 - 100, 32, "")
    input_boxes_a = [text_input_boxa1, text_input_boxa2]

    text_input_boxb1 = InputBox(250, 100, width/2 - 100, 32, "")
    text_input_boxb2 = InputBox(250, 200, width/2 - 100, 32, "")
    text_input_boxb3 = InputBox(250, 300, width/2 - 100, 32, "")
    text_input_boxb4 = InputBox(250, 400, width/2 - 100, 32, "")
    input_boxes_b = [text_input_boxb1, text_input_boxb2, text_input_boxb3, text_input_boxb4]

    text_input_boxc1 = InputBox(0, 700, width/2 - 100, 32, "U")
    text_input_boxc2 = InputBox(0, 733, width/2 - 100, 32, "C")
    input_boxes_c = [text_input_boxc1, text_input_boxc2]

    text = ''
    font2 = pygame.font.Font(None, 32)
    user = passwd = newuser = newpasswd = ''

    running=True
    start = False
    login = False
    created = False
    option = 0
    already_here = False
    msg = ''

    while running:
        if option  == 0:
            running, option = landingPage()
        elif option == 1 or option == 3:
            login = False
            already_here = False
            input_boxes_a[0].done = False
            input_boxes_a[1].done = False

            if login == False:
                screen.fill(BLACK)

                rect1 = pygame.Rect(300, 100, 170, 28)
                txt_surface = FONT.render('Usuario', True, 'white')
                screen.blit(txt_surface, (300, 100))
                pygame.draw.rect(screen, 'black', rect1, 2)

                rect2 = pygame.Rect(280, 300, 170, 28)
                txt_surface = FONT.render('Contraseña', True, 'white')
                screen.blit(txt_surface, (285, 300))
                pygame.draw.rect(screen, 'black', rect2, 2)

                create = pygame.Rect(310, 500, 170, 32)

                if option == 1:
                    txt_surface = FONT.render('Crear', True, 'orange')
                elif option == 3:
                   txt_surface = FONT.render('Borrar', True, 'red')

                screen.blit(txt_surface, (310+5, 500+5))
                pygame.draw.rect(screen, 'black', create, 2)

                txt_msg = FONT.render("", True, 'yellow')
                screen.blit(txt_msg, (280+5, 600+5))

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if create.collidepoint(event.pos):
                            for box in input_boxes_a:
                                print(box.text)
                                box.done = True
                                box.textcopy = box.text
                                box.text = ''
                    for box in input_boxes_a:
                        box.handle_event(event)

                if input_boxes_a[0].done == True:
                    user = input_boxes_a[0].textcopy
                if input_boxes_a[1].done == True:
                    passwd = input_boxes_a[1].textcopy

                if user != '' and passwd != '':
                    if already_here == False:
                        with MySocket("TCP", ADDR) as client:
                            if option == 1:
                                client.send_msg("Create")
                                client.send_obj((user,passwd))
                                msg = client.recv_msg()
                                already_here = True
                                login = True
                                option = 0
                                txt_msg = FONT.render(msg, True, 'yellow')
                                screen.blit(txt_msg, (20, 600))
                                pygame.display.update()
                                time.sleep(2)
                            elif option == 3:
                                client.send_msg("Delete")
                                client.send_obj((user,passwd))
                                msg = client.recv_msg()
                                already_here = True
                                login = False
                                option = 0
                                txt_msg = FONT.render(msg, True, 'yellow')
                                screen.blit(txt_msg, (20, 600))
                                pygame.display.update()
                                time.sleep(2)

                    user = ''
                    passwd = ''

                for box in input_boxes_a:
                    box.update()
                    box.draw(screen, login)

            pygame.display.flip()
            clock.tick(20)

        elif option == 2:
            login = False
            already_here = False
            input_boxes_b[0].done = False
            input_boxes_b[1].done = False
            input_boxes_b[2].done = False
            input_boxes_b[3].done = False

            if login == False:
                screen.fill(BLACK)

                rect1 = pygame.Rect(300, 60, 170, 28)
                txt_surface = FONT.render('Nombre', True, 'white')
                screen.blit(txt_surface, (300, 65))
                pygame.draw.rect(screen, 'black', rect1, 2)

                rect2 = pygame.Rect(280, 160, 170, 28)
                txt_surface = FONT.render('Contraseña', True, 'white')
                screen.blit(txt_surface, (285, 165))
                pygame.draw.rect(screen, 'black', rect2, 2)

                rect3 = pygame.Rect(270, 270, 170, 20)
                txt_surface = FONT.render('Nuevo nombre', True, 'white')
                screen.blit(txt_surface, (270, 270))
                pygame.draw.rect(screen, 'black', rect3, 2)

                rect4 = pygame.Rect(250, 370, 170, 20)
                txt_surface = FONT.render('Nueva contraseña', True, 'white')
                screen.blit(txt_surface, (255, 370))
                pygame.draw.rect(screen, 'black', rect4, 2)

                edit = pygame.Rect(310, 500, 170, 32)
                txt_surface = FONT.render('Editar', True, 'green')
                screen.blit(txt_surface, (310+5, 500+5))
                pygame.draw.rect(screen, 'black', edit, 2)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if edit.collidepoint(event.pos):
                            for box in input_boxes_b:
                                print(box.text)
                                box.done = True
                                box.textcopy = box.text
                                box.text = ''
                    for box in input_boxes_b:
                        box.handle_event(event)

                if input_boxes_b[0].done == True:
                    user = input_boxes_b[0].textcopy
                if input_boxes_b[1].done == True:
                    passwd = input_boxes_b[1].textcopy
                if input_boxes_b[2].done == True:
                    newuser = input_boxes_b[2].textcopy
                if input_boxes_b[3].done == True:
                    newpasswd = input_boxes_b[3].textcopy

                if user != '' and passwd != '' and newuser != '' and newpasswd != '':
                    if already_here == False:
                        with MySocket("TCP", ADDR) as client:
                            client.send_msg("Update")
                            client.send_obj((user,passwd))
                            client.send_obj((newuser,newpasswd))
                            msg = client.recv_msg()
                            already_here = True
                            login = True
                            option = 0
                            txt_msg = FONT.render(msg, True, 'yellow')
                            screen.blit(txt_msg, (20, 600))
                            pygame.display.update()
                            time.sleep(2)
                    user = passwd = newuser = newpasswd = ''

                for box in input_boxes_b:
                    box.update()
                    box.draw(screen, login)

            pygame.display.flip()
            clock.tick(20)

        elif option == 4:
            login = False
            already_here = False
            input_boxes_c[0].done = False
            input_boxes_c[1].done = False
            if login == False:
                fuente= pygame.font.Font(None, 30)
                texto= fuente.render("", True, BLACK)
                screen.blit(texto, [width-120, AA_Engine.Map.SIZE*(TAM+MARGEN)+MARGEN+15])

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    for box in input_boxes_c:
                        box.handle_event(event)

                if input_boxes_c[0].done == True:
                    user = input_boxes_c[0].textcopy
                if input_boxes_c[1].done == True:
                    passwd = input_boxes_c[1].textcopy

                if user != '' and passwd != '':
                    if already_here == False:
                        with MySocket("TCP", ADDR) as client:
                            print("bbbbb")
                            client.send_msg("Create")
                            client.send_obj((user,passwd))
                            print(client.recv_msg())
                            already_here = True
                            login = True

                for box in input_boxes_c:
                    box.update()
                    box.draw(screen, login)

            if login == True:

                if created == False:
                    player = game.newPlayer(input_boxes_c[0].textcopy, AA_Engine.Cell(x, y))
                    created = True

                fuente= pygame.font.Font(None, 30)
                texto= fuente.render("Nivel: "+str(player.getLevel()), True, YELLOW)
                screen.blit(texto, [width-120, AA_Engine.Map.SIZE*(TAM+MARGEN)+MARGEN+15])

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
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
