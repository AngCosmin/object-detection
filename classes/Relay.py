import ConfigParser
import RPi.GPIO as GPIO

class Relay:
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            self.PIN_RELAY = config.getint('Relay', 'pin')

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.PIN_RELAY, GPIO.OUT)
        except Exception as e:
            print e
        
    def turn_on(self):
        GPIO.setmode(GPIO.BOARD)        
        GPIO.output(self.PIN_RELAY, GPIO.LOW)

    def turn_off(self):
        GPIO.setmode(GPIO.BOARD)        
        GPIO.output(self.PIN_RELAY, GPIO.HIGH)        