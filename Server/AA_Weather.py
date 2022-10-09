'''
- ARGS:
    - Puerto de escucha
- RETURNS:
    - {ciudad:, temperatura:}, aleatoriamente de una BD
'''

import socket, sys, pickle, random, csv

ADDR = ("", int(sys.argv[1]))

FDATA_WEATHERS = "./data/weathers.csv"

def get_weathers():
    with open(FDATA_WEATHERS , "r") as f:
        for line in csv.reader(f, delimiter=";"):
            yield {"ciudad":line[0], "temperatura":line[1]}

weathers = list(get_weathers())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

while True:
    conn, direcc = server.accept()
    print(direcc, "Solicita ciudad y temperatura")

    weather = random.choice(weathers)
    conn.sendall(pickle.dumps(weather))
    print(direcc, "Obtiene", weather)

    conn.close()

server.close()