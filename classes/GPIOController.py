import RPi.GPIO as GPIO
from time import sleep
from classes.MotorsController import MotorsController

class GPIOController:
    @staticmethod
    def clean():
        GPIO.cleanup()                
