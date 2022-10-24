"""
client.recv_obj()
"""

from common_utils import MySocket

from dataclasses import dataclass, asdict
import sys, random
import csv


ADDR = ("", int(sys.argv[1]))

FDATA_WEATHERS = "../data/weathers.csv"


@dataclass
class Weather:
    city: str
    temperature: float


def get_weathers():
    with open(FDATA_WEATHERS , "r") as f:
        for line in csv.reader(f, delimiter=";"):
            yield asdict(Weather(line[0], float(line[1])))

#==================================================

with MySocket("TCP", ADDR) as server:
    weathers = list(get_weathers())

    while True:
        conn, direcc = server.accept()
        print(direcc, "Solicita ciudad y temperatura")

        weather = random.choice(weathers)
        server.send_obj(weather)
        print(direcc, "Obtiene", weather)

        conn.close()