import RPi.GPIO as g
from time import sleep

pump1 = 25
pump2 = 8
pump3 = 7
pump4 = 1
pumps = [pump1, pump2, pump3, pump4]

def setup():
    g.setwarnings(False)
    g.setmode(g.BCM)
    for pump in pumps:
        g.setup(pump, g.OUT)
        g.output(pump, False)
