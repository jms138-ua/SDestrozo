import sys, pickle, os
import random
import time, platform
from threading import Thread
from random import randrange
from common_utils import MySocket
from kafka import KafkaConsumer, KafkaProducer

ADDR_R = (sys.argv[1].split(":")[0], int(sys.argv[1].split(":")[1]))
ADDR_E = (sys.argv[2].split(":")[0], int(sys.argv[2].split(":")[1]))
ADDR_K = [sys.argv[3]+":29092"]

class bcolors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    GRAY = "\033[0;37m"
    BROWN = "\033[0;33m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    BLINK = "\033[5m"
    WHITE = "\033[0;37m"
    END = "\033[0m"

def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def printLeaderBoard(mapa):
    print("***********************************")
    print("*       TABLA DE CAMPEONES        *")
    print("***********************************")

    players = sorted_players = []
    SIZE = 20
    i = 0
    champion = ""
    color = bcolors.WHITE

    for fil in range(SIZE):
        for col in range(SIZE):
            if mapa[fil][col] != "M" and mapa[fil][col] != " " and mapa[fil][col] != "A":
                othersym = mapa[fil][col][0]
                alias = othersym[0]
                if len(alias) >= SIZE - 2:
                    alias = alias[0:SIZE - 2] + "..."
                level = str(othersym[1])

                players.append((alias,level))

    sorted_players = list(sorted(players, key=lambda x: x[1], reverse=True))

    for (x,y) in sorted_players:
        i+=1
        if i == 1:
            color = bcolors.YELLOW
        else:
            color = bcolors.WHITE
        print(color + str(i) + " - " + x + ": nivel " + y + bcolors.END)

    print("***********************************")

    if len(sorted_players) == 1:
        clear_console()
        for (x,y) in sorted_players:
            champion = x.upper()
        print(bcolors.GREEN+champion+" ha ganado el derecho de presumir"+bcolors.END)
        time.sleep(2)
        clear_console()
        exit()

def printMap(mapa):
    clear_console()
    color = bcolors.BLACK

    printLeaderBoard(mapa)

    for fil in range(20):
        for col in range(20):
            if fil < 10 and col < 10:
                color = bcolors.LIGHT_GREEN
            elif fil < 10 and col >= 10:
                color = bcolors.LIGHT_BLUE
            elif fil >= 10 and col < 10:
                color = bcolors.RED
            else:
                color = bcolors.GRAY
            if mapa[fil][col] == "M":
                symbol = "#"
            elif mapa[fil][col] == " ":
                symbol = "·"
            elif mapa[fil][col] == "A":
                symbol = "+"
            else:
                othersym = mapa[fil][col][0]
                symbol = othersym[0:1]
                othersym = symbol[0]
                symbol = othersym[0:1].upper()
                color = bcolors.YELLOW
            print(color+"%%-%ds" % 2 % symbol+bcolors.END, end="")
        print()

def getDirec(cardinal):
    tuplita = (0,0)

    if cardinal == "N":
        tuplita = (0,-1)
    elif cardinal == "S":
        tuplita = (0,1)
    elif cardinal == "W":
        tuplita = (-1,0)
    elif cardinal == "E":
        tuplita = (1,0)
    elif cardinal == "SE":
        tuplita = (1,1)
    elif cardinal == "SW":
        tuplita = (-1,1)
    elif cardinal == "NE":
        tuplita = (1,-1)
    elif cardinal == "NW":
        tuplita = (-1,-1)
    else:
        tuplita = (0,0)

    return tuplita

def funcsend(alias):
    producer = KafkaProducer(
        bootstrap_servers = ADDR_K,
        value_serializer = lambda v: pickle.dumps(v)
    )
    i = (0,0)
    direc = ""
    cardinal = ""
    alive = True
    while alive:
        direc = input()
        if direc.upper() == "W":
            cardinal = "N"
        elif direc.upper() == "A":
            cardinal = "W"
        elif direc.upper() == "S":
            cardinal = "S"
        elif direc.upper() == "D":
            cardinal = "E"
        elif direc.upper() == "Q":
            cardinal = "NW"
        elif direc.upper() == "C":
            cardinal = "SE"
        elif direc.upper() == "E":
            cardinal = "NE"
        elif direc.upper() == "X":
            cardinal = "SW"
        i = getDirec(cardinal)
        data = {alias:i}
        if i != (0,0):
            producer.send('movement', value=data)
        i = (0,0)
        direc = ""
        cardinal = ""

def funcrecv(ini_map, alias):
    consumer = KafkaConsumer(
     "map",
     bootstrap_servers=ADDR_K,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=alias,
     value_deserializer = lambda v: pickle.loads(v)
    )

    printMap(ini_map)
    for msg in consumer:
        mapa = list(msg.value.values())[0]
        printMap(mapa)

def startMatch(alias, mapa):
    Thread(target=funcrecv, args=(mapa,alias,), daemon=True).start()
    t2 = Thread(target=funcsend, args=(alias,), daemon=True)
    t2.start()
    t2.join()
    time.sleep(1)

def getReady(alias):
    mapa = None

    clear_console()
    print(bcolors.RED+"Esperando a jugadores, no salgas de la partida"+bcolors.END)

    consumer = KafkaConsumer(
     "map",
     bootstrap_servers=ADDR_K,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=alias,
     consumer_timeout_ms= 60 * 30 * 1000,
     value_deserializer = lambda v: pickle.loads(v)
    )

    mustend = time.time() + 60 * 30
    if time.time() < mustend:
        msg = next(consumer)
        mapa = list(msg.value.values())[0]

    return mapa

def printMsg(msg):
    if msg[0:5] == "Error":
        print(bcolors.YELLOW+msg+bcolors.END)
    else:
        print(bcolors.GREEN+msg+bcolors.END)

def checkUserData(username, password):
    alias = passwd = name = ""
    chars = False

    alias = ''.join(e for e in username if e.isalnum())
    passwd = ''.join(e for e in password if e.isalnum())

    for e in alias:
        if e.isnumeric() and chars == False:
            pass
        else:
            chars = True
            name = name + e
        chars = False

    if name != "" and passwd != "":
        return name, passwd
    else:
        print(bcolors.YELLOW+"Error, campo vacío"+bcolors.END)
        return "", ""

def createUser():
    clear_console()
    print('- Crear usuario -')
    confirmation = username = password = usr = passwd = ""

    while confirmation != "S" and confirmation != "s":
        confirmation = ""
        username = input("¿Cómo te llamamos?: ")
        password = input("Escribe una contraseña: ")

        usr, passwd = checkUserData(username, password)
        if usr != "" and passwd != "":
            while confirmation != "S" and confirmation != "s" and confirmation != "N" and confirmation != "n":
                confirmation = input("¿Quieres registrarte con estos datos? ["+ usr +","+passwd+"] (s/n): ")

            if confirmation == "S" or confirmation == "s":
                client = MySocket("TCP", ADDR_R)
                client.send_msg("Create")
                client.send_obj((usr,passwd))
                msg = client.recv_msg()
                printMsg(msg)
                client.close()

        username = password = usr = passwd = ""

def editUser():
    clear_console()
    print('- Editar perfil -')
    username = password = newuser = newpasswd = usr = passwd = ""

    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")
    newuser = input("Nuevo nombre: ")
    newpasswd = input("Nueva contraseña: ")

    usr, passwd = checkUserData(newuser, newpasswd)

    if username == usr and password == passwd:
        print(bcolors.YELLOW+"No hay nada que cambiar"+bcolors.END)
    else:
        client = MySocket("TCP", ADDR_R)
        client.send_msg("Update")
        client.send_obj((username,password))
        client.send_obj((usr,passwd))
        msg = client.recv_msg()
        printMsg(msg)
        client.close()

def deleteUser():
    clear_console()
    print('- Borrar usuario -')
    username = password = usr = passwd = ""

    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    usr, passwd = checkUserData(username, password)
    if usr != "" and passwd != "":
        client = MySocket("TCP", ADDR_R)
        client.send_msg("Delete")
        client.send_obj((usr,passwd))
        msg = client.recv_msg()
        printMsg(msg)
        client.close()

def login():
    clear_console()
    print('- Iniciar sesión -')
    username = password = usr = passwd = ""
    login = False
    ready = "A"
    mapa = None

    username = input("Nombre de usuario: ")
    password = input("Contraseña: ")

    usr, passwd = checkUserData(username, password)
    if usr != "" and passwd != "":
        client = MySocket("TCP", ADDR_E)
        client.send_msg("Player")
        client.send_obj((usr,passwd))
        msg = client.recv_msg()
        printMsg(msg)
        if msg[0:5] != "Error":
            while ready != "":
                ready = input("Presiona ENTER cuando esté todo listo: ")
            client.send_msg("Ready")
            mapa = getReady(usr)
            startMatch(usr, mapa)

def optionError():
    print(bcolors.YELLOW+'Operación incorrecta. Escribe un número entre 1 y 5.'+bcolors.END)

menu_options = {
    1: 'Crear usuario',
    2: 'Editar perfil',
    3: 'Borrar perfil',
    4: 'Iniciar sesión',
    5: 'Salir',
}

def print_menu():
    for key in menu_options.keys():
        print (key, '-', menu_options[key])

def main():
    option = 0
    exc = False
    while(True):
        time.sleep(2)
        clear_console()
        print("- Menú de SDestrozo -")
        print_menu()
        try:
            option = int(input('Escoge una operación: '))
        except:
            exc = True
            optionError()
        if option == 1:
            createUser()
        elif option == 2:
            editUser()
        elif option == 3:
            deleteUser()
        elif option == 4:
            login()
        elif option == 5:
            print(bcolors.CYAN+'Vuelve pronto'+bcolors.END)
            time.sleep(1)
            clear_console()
            exit()
        else:
            if exc == False:
                optionError()
        exc = False
        option = 0

if __name__ == '__main__':
    main()
