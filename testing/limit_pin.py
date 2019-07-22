import RPi.GPIO as GPIO
import time

limit_pin = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(limit_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while not GPIO.input(limit_pin):
    print("low")
while GPIO.input(limit_pin):
    print("high")

