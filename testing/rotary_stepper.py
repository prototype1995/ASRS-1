import RPi.GPIO as GPIO
from time import sleep

pinA = 13
pinB = 15

lastEncoded = 0
encoderVal = 0

last_encoder_val = 0

last_MSB = 0
last_LSB = 0

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pinA , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pinB , GPIO.IN, pull_up_down=GPIO.PUD_UP)

dec_bits  = [0b1101, 0b0100, 0b0010, 0b1011]
inc_bits = [0b1110, 0b0111, 0b0001, 0b1000]



def update_encoder(pin):
    """
    Updates the angular position.
    """
    global lastEncoded
    global encoderVal
    global last_MSB
    global last_LSB
    MSB = GPIO.input(pinA)
    LSB = GPIO.input(pinB)

    encoded = (MSB<<1) | LSB
    print(last_MSB, last_LSB, MSB, LSB)
    
    sum1 = (lastEncoded<<2)|encoded
    
    
    if sum1 in inc_bits:
    #if format(sum, "#006b") in inc_bits:
        encoderVal += 1
    
    #if format(sum, "#006b") in dec_bits:
    if sum1 in dec_bits:
        encoderVal -= 1
    
    print(sum1, encoderVal)

    lastEncoded = encoded; #store this value for next time.


GPIO.add_event_detect(pinA, GPIO.BOTH, callback=update_encoder)
GPIO.add_event_detect(pinB, GPIO.BOTH, callback=update_encoder)

while True:
    sleep(1)
