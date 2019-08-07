import logging
import serial
import serial.tools.list_ports as ports
import threading

logger = logging.getLogger(__name__)


import RPi.GPIO as GPIO
import time

class StepperMotor:
    """
    Control the stepper motors
    """
    def __init__(self, step_pin=21, dir_pin=20, limit_pin=16, step_angle = 1.8,
                 stepping = 16, delay=0.0001, res=0.005):
        """
        Intialize the StepperMotor object
        Args: int step_pin
              int dir_pin
              int sleep_pin
              Defualts: step_pin=20, dir_pin=21, limit_pin=10, step_angle = 1.8
        Returns: None
        """
        self.CW = 0
        self.CCW = 1
        #Micro Stepping Config
        # MS1 MS2 MS3 - Step Resolution - self.stepping
        # L L L - Full Step - 1
        # H L L - Half Step - 2
        # L H L - Quater Step - 4
        # H H L - Eighth Step - 8
        # H H H - Sixteenth Step - 16
        self.stepping = stepping #eighth stepping
        self.SPR = int(360/step_angle)*self.stepping #steps per revolution - *4 for quater stepping
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.limit_pin = limit_pin
        self.res = res
        self.delay =  delay

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(step_pin, GPIO.OUT)
        GPIO.setup(dir_pin, GPIO.OUT)
        GPIO.setup(limit_pin , GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def drive_motor(self, delay=None, revolutions=None, direction=0):
        """
        Funtion to drive stepper motor
        Args: int duration - time duration in seconds - defualt 2
              int revolutions - no. of revolutions to complete - default 1
              int dir - CW or CCW - defualt CW - 0
        """
        if delay is None:
            delay=self.delay
        if revolutions is None:
            res = self.res
    
        GPIO.output(self.dir_pin, direction)

        steps = int(revolutions*self.SPR)
        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)
    

    def go_home(self, delay=None, res=None):
        """
        Method to home motor
        TODO: go_home() not adaptable
        pusher motor: go_home(delay=0.001, res=1)
        """
        if delay is None:
            delay = self.delay
        if res is None:
            res = self.res

        home_dir = self.CW
        while not GPIO.input(self.limit_pin):
            self.drive_motor(delay=delay, revolutions=res, direction=home_dir)
            

    def deccelerate(self, rate=1.0):
        """
        Deccelerate before braking
        ARGS: float rate - decceleration rate
        """

        delay = self.delay
        steps = int(revolutions*self.SPR)
        GPIO.output(self.dir_pin, direction)
        for i in range(steps):
            delay = delay + rate*delay #deccelerate
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

    def set_curr_pos(self, pos=0.0):
        """
        Setter function for curr_pos
        Args: pos in degrees
        """
        self.curr_pos = pos


    def sleep(self):
        """
        Activate the sleep mode - sets the sleep pin to GPIO.LOW
        """
        pass

    def wake():
        """
        Deactivate the sleep mode - sets the sleep pin to GPIO.HIGH
        """
        pass


class Solenoid:
    """
    Switch the solenoid pin

    """
    def __init__(self, in1_pin=17):
        self.in1_pin = in1_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(in1_pin , GPIO.OUT)
        GPIO.output(self.in1_pin, GPIO.LOW)

    def fire_solenoid(self, duration=3):
        """"""
        GPIO.output(self.in1_pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.in1_pin, GPIO.LOW)


class LED:
    """
    Switch the LED.
    """
    def __init__(self, in1_pin=32):
        self.in1_pin = in1_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(in1_pin , GPIO.OUT)
        GPIO.output(self.in1_pin, GPIO.LOW)

    def fire_led(self, state=False):
        """
        Method to turn on and off LED according to state.
        """
        if state:
            GPIO.output(self.in1_pin, GPIO.HIGH)
        else:
            GPIO.output(self.in1_pin, GPIO.LOW)
