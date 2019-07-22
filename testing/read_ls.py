import RPi.GPIO as g
import time

g.setmode(g.BOARD)
ls_pin = 37
g.setup(ls_pin, g.IN)
print(g.input(ls_pin))
time.sleep(1)
