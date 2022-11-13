import sys, random, time, pickle
from threading import Thread
from common_utils import MySocket
from kafka import KafkaConsumer, KafkaProducer

ADDR_KAFKA = [sys.argv[1]+":29092"]
ADDR_E = (sys.argv[2].split(":")[0], int(sys.argv[2].split(":")[1]))

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
        bootstrap_servers = ADDR_KAFKA,
        value_serializer = lambda v: pickle.dumps(v)
    )
    i = (0,0)
    direc = ""
    res = ""
    alive = True
    while alive:
        time.sleep(2)
        direc=["N","S","W","E","NE","SW","NW","SE"]
        random_idx = random.randint(0,7)
        res = direc[random_idx]
        i = getDirec(res)
        data = {alias:i}
        if i != (0,0):
            producer.send('movement', value=data)
        i = (0,0)
        direc = ""
        res = ""
        time.sleep(2)

def funcrecv(alias):
    consumer = KafkaConsumer(
     "map",
     bootstrap_servers=ADDR_KAFKA,
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=alias,
     value_deserializer = lambda v: pickle.loads(v)
    )

    for msg in consumer:
        mapa = list(msg.value.values())[0]

def getReady():
    usr = "@NPC"
    client = MySocket("TCP", ADDR_E)
    client.send_msg("NPC")
    client.send_obj(usr)
    msg = client.recv_msg()

    return usr

if __name__=="__main__":
    alias = getReady()
    Thread(target=funcrecv, args=(alias,), daemon=True).start()
    t2 = Thread(target=funcsend, args=(alias,), daemon=True)
    t2.start()
    t2.join()
    print("he salido de la pista")
    time.sleep(10000)
