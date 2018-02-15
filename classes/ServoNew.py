import ConfigParser
import time
import pigpio

class ServoNew:
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            self.PIN = config.getint('Servo', 'pin')

            self.pi = pigpio.pi()
            self.pi.set_mode(self.PIN, pigpio.OUTPUT)
        except Exception as e:
            print e
    
    def change(self, value):
        print 'Servo to ' + str(value)
        # self.pi.set_servo_pulsewidth(self.PIN, value)
        # self.pi.get_servo_pulsewidth(self.PIN, value)

    def clean(self):
        self.pi.stop()