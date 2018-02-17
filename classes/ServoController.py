import ConfigParser
import pigpio
from time import sleep
from classes.Servo import Servo

class ServoController:
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')
            pin = config.getint('Servo', 'pin_GPIO')

            self.head = Servo(pin)
            self.servoValue = 1500
            self.head.change(1500)
        except Exception as e:
            print e

    def change(self, value):
        self.servoValue = value
        self.head.change(value)
    
    def compute(self, object_y):
        if abs(object_y) > 10:
            oldServoValue = self.servoValue
            self.servoValue = self.servoValue + object_y * 0.75

            if self.servoValue < 1000:
                self.servoValue = 1000
            elif self.servoValue > 2000:
                self.servoValue = 2000

            if oldServoValue != self.servoValue:
                self.head.change(self.servoValue)

    def clean(self):
        print '[PINS] Cleaning up servo pins...'
        self.head.clean()
        sleep(0.2)
    