import ConfigParser
import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self):
        # Get motors pins from config file
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            self.PIN = config.getint('Servo', 'pin')

            # Set GPIO mode
            GPIO.setmode(GPIO.BOARD)

            # Setup pins
            GPIO.setup(self.PIN, GPIO.OUT)

            self.PWM_servo = GPIO.PWM(self.PIN, 50)         

            self.PWM_servo.start(7.5);
        except Exception as e:
            print e
    
    def changeDutyCycle(self, value):
        self.PWM_servo.ChangeDutyCycle(value)
        GPIO.output(self.PIN, GPIO.LOW)        

    def cleanup_pins(self):
        print '[PINS] Cleaning up pins...'
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.output(self.PIN, GPIO.LOW)

        time.sleep(1)
        GPIO.cleanup()
        print '[PINS] Done!'