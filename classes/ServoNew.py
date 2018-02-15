import ConfigParser
import time
import pigpio

class ServoNew:
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            self.PIN = config.getint('Servo', 'pin_GPIO')

            self.pi = pigpio.pi()
            self.pi.set_mode(self.PIN, pigpio.OUTPUT)
        except Exception as e:
            print e
    
    def change(self, value):
        self.pi.set_servo_pulsewidth(self.PIN, value)

    def clean(self):
        self.pi.stop()