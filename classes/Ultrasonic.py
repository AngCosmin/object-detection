import RPi.GPIO as GPIO
from time import time
from time import sleep

class Ultrasonic:
    def __init__(self, echo_pin, trig_pin):
        self.echo_pin = echo_pin
        self.trig_pin = trig_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.trig_pin, GPIO.OUT)

    def measure(self):
        GPIO.output(self.trig_pin, False)
        GPIO.output(self.trig_pin, True)
        sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        while GPIO.input(self.echo_pin) == 0:
            print 'Measure 0'
            pulse_start = time()
        
        while GPIO.input(self.echo_pin) == 1:
            print 'Measure 1'            
            pulse_end = time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

        return distance

    def clean(self):
        GPIO.output(self.trig_pin, False)

    

    