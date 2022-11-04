import sys, random, time

'''
    PENDIENTE:
        - Kafka: enviar cada movimiento
'''

class NPC():
    # no le afecta la temperatura ni cambia de nivel
    def __init__(self, alias, category):
        self.alias = alias
        self.pos = (-1,-1) # una cell o algo
        # la categoría es por eso del npc que persigue y el que no
        # categoría sería tipo 1 o 2, pero si ves que meh bórralo
        self.category = category
        self.__level = random.randint(8,12)

    def __str__(self):
        return "NPC " + self.alias + ", con nivel " + str(self.getTotalLevel())

    # el NPC sólo puede morir si entra en una pelea con jugadores -> (y entre npcs qué? npi)
    def isAlive(self):
        return self.__level != -1

    def die(self):
        self.__level = -1

    # nada de cambios por temperatura, recuerda
    def getTotalLevel(self):
        return self.__level

    def getAlias(self):
        return self.alias

    def getCategory(self):
        return self.category

    def getPos(self):
        return self.pos

def distancia_manhattan(origen,destino):
    distancia = 0

    abs_x = abs(destino.getFila()-origen.getFila())
    abs_y = abs(destino.getCol()-origen.getCol())

    distancia = abs_x + abs_y

    return distancia

def orientation(npc, player):
    ori = ""
    abs_x = abs(player.getFila()-npc.getFila())
    abs_y = abs(player.getCol()-npc.getCol())

    if abs_x == 0:
        if abs_y > 0:
            ori = "S"
        elif abs_y < 0:
            ori = "N"
    elif abs_x < 0:
        if abs_y > 0:
            ori = "SW"
        elif abs_y == 0:
            ori = "W"
        elif abs_y < 0:
            ori = "NW"
    elif abs_x > 0:
        if abs_y > 0:
            ori = "SE"
        elif abs_y == 0:
            ori = "E"
        elif abs_y < 0:
            ori = "NE"

    return ori

# de momento los NPCs pares no se mueven porque no buscan
# mientras que los NPCs impares se mueven al azar
def move(npc, cat):
    direc=["N","S","W","E","NE","SW","NW","SE"]
    res = ""
    d_min = 99999
    d = 99999
    idx = 0
    idx_min = 0

    if cat == False:
        random_idx = random.randint(0,7)
        res = direc[random_idx]
        print(npc.getAlias() + " se mueve hacia el: "+ direc[random_idx])
    else:
        pass
        '''
        for p in players:
            d = distancia_manhattan(npc.getPos(), p.getPos())
            idx = idx + 1
            if d < d_min:
                d_min = d
        idx_min = idx

        res = orientation(npc.getPos(), players[idx_min].getPos())
        '''

    return res

if __name__=="__main__":
    npc = None
    npcs = []
    i = 0
    superNPC = False # superNPC es la categoría

    # cada 10" crea un NPC cheto o random que se mueve cada [0,1] segundos
    while True:
        superNPC = not superNPC
        npc = NPC("NPC"+str(i), superNPC)
        npcs.append(npc)
        i = i + 1
        print("soy "+ npc.getAlias() + " y estoy chetísimo")
        for n in npcs:
            move(n,n.getCategory())
            time.sleep(random.uniform(0, 1))
        time.sleep(10)
