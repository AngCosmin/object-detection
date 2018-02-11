import ConfigParser
import RPi.GPIO as GPIO
from classes.Motor import Motor
from time import sleep

class MotorsController:
    def __init__(self):
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            PIN_1_LEFT = config.getint('MotorLeft', 'pin_1') 
            PIN_2_LEFT = config.getint('MotorLeft', 'pin_2')
            PIN_PWM_LEFT = config.getint('MotorLeft', 'pin_pwm')

            PIN_1_RIGHT = config.getint('MotorRight', 'pin_1')
            PIN_2_RIGHT = config.getint('MotorRight', 'pin_2')
            PIN_PWM_RIGHT = config.getint('MotorRight', 'pin_pwm')

            self.PIN_RELAY = config.getint('Relay', 'pin')

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.PIN_RELAY, GPIO.OUT)
            
            self.left = Motor(PIN_1_LEFT, PIN_2_LEFT, PIN_PWM_LEFT)
            self.right = Motor(PIN_1_RIGHT, PIN_2_RIGHT, PIN_PWM_RIGHT)         
        except Exception as e:
            print e

    def stop(self):
        self.left.stop()
        self.right.stop()

    def move_motors(self, left_speed, right_speed):
        print 'Motor left speed ' + str(left_speed) + ' Motor right speed ' + str(right_speed)  
        self.left.move(left_speed)
        self.right.move(right_speed)                

    def toggleMotors(self, status):
        if status == 'on': 
            GPIO.output(self.PIN_RELAY, GPIO.LOW)
        else:
            GPIO.output(self.PIN_RELAY, GPIO.HIGH)

    def clean(self):
        print '[PINS] Cleaning up pins...'
        self.left.clean()
        self.right.clean()
        GPIO.output(self.PIN_RELAY, GPIO.HIGH)
        sleep(1)
        GPIO.cleanup()        
        print '[PINS] Done!'