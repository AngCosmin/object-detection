import ConfigParser
import RPi.GPIO as GPIO
import time

class Motors:
    def __init__(self):
        # Get motors pins from config file
        config = ConfigParser.RawConfigParser()

        try:
            config.read('./config.cfg')

            self.PIN_1_LEFT = config.getint('MotorLeft', 'pin_1') 
            self.PIN_2_LEFT = config.getint('MotorLeft', 'pin_2')
            self.PIN_PWM_LEFT = config.getint('MotorLeft', 'pin_pwm')

            self.PIN_1_RIGHT = config.getint('MotorRight', 'pin_1')
            self.PIN_2_RIGHT = config.getint('MotorRight', 'pin_2')
            self.PIN_PWM_RIGHT = config.getint('MotorRight', 'pin_pwm')

            self.PIN_RELAY = config.getint('Relay', 'pin')

            # Set GPIO mode
            GPIO.setmode(GPIO.BOARD)

            # Setup pins
            GPIO.setup(self.PIN_1_LEFT, GPIO.OUT)
            GPIO.setup(self.PIN_2_LEFT, GPIO.OUT)
            GPIO.setup(self.PIN_PWM_LEFT, GPIO.OUT)

            GPIO.setup(self.PIN_1_RIGHT, GPIO.OUT)
            GPIO.setup(self.PIN_2_RIGHT, GPIO.OUT)
            GPIO.setup(self.PIN_PWM_RIGHT, GPIO.OUT)

            GPIO.setup(self.PIN_RELAY, GPIO.OUT)

            self.PWM_left = GPIO.PWM(self.PIN_PWM_LEFT, 100)         
            self.PWM_right = GPIO.PWM(self.PIN_PWM_RIGHT, 100)

            self.PWM_left.start(0);
            self.PWM_right.start(0);            
        except Exception as e:
            print e

    def move_motors(self, motorLeftSpeed, motorRightSpeed, direction):
        print 'Motor left speed ' + str(motorLeftSpeed) + ' Motor right speed ' + str(motorRightSpeed)  

        motorLeftSpeed = abs(motorLeftSpeed)
        motorRightSpeed = abs(motorRightSpeed)

        if motorLeftSpeed == 0:
            self.stop_left()
        else:
            self.PWM_left.ChangeDutyCycle(motorLeftSpeed)
            self.activate_motor_left_pins(direction)

        if motorRightSpeed == 0:
            self.stop_right()
        else:
            self.PWM_right.ChangeDutyCycle(motorRightSpeed)
            self.activate_motor_right_pins(direction)


    def stop_left(self):
        GPIO.output(self.PIN_1_LEFT, False)
        GPIO.output(self.PIN_2_LEFT, False)
        GPIO.output(self.PIN_PWM_LEFT, False)

    def stop_right(self):
        GPIO.output(self.PIN_1_RIGHT, False)
        GPIO.output(self.PIN_2_RIGHT, False)
        GPIO.output(self.PIN_PWM_RIGHT, False)

    def activate_motor_left_pins(self, direction):
        if direction == 'forward':
            GPIO.output(self.PIN_1_LEFT, False)
            GPIO.output(self.PIN_2_LEFT, True)
            GPIO.output(self.PIN_PWM_LEFT, True)
        elif direction == 'backward':
            GPIO.output(self.PIN_1_LEFT, True)
            GPIO.output(self.PIN_2_LEFT, False)
            GPIO.output(self.PIN_PWM_LEFT, True) 
            
    def activate_motor_right_pins(self, direction):
        if direction == 'forward':
            GPIO.output(self.PIN_1_RIGHT, False)
            GPIO.output(self.PIN_2_RIGHT, True)
            GPIO.output(self.PIN_PWM_RIGHT, True)
        elif direction == 'backward':
            GPIO.output(self.PIN_1_RIGHT, True)
            GPIO.output(self.PIN_2_RIGHT, False)
            GPIO.output(self.PIN_PWM_RIGHT, True) 
    
    def toggleMotors(self, status):
        if status == 'on': 
            GPIO.output(self.PIN_RELAY, GPIO.LOW)
        else:
            GPIO.output(self.PIN_RELAY, GPIO.HIGH)

    def cleanup_pins(self):
        print '[PINS] Cleaning up pins...'
        GPIO.setmode(GPIO.BOARD)
        
        # Cleanup PINs for motor left
        GPIO.output(self.PIN_1_LEFT, GPIO.LOW)
        GPIO.output(self.PIN_2_LEFT, GPIO.LOW)
        GPIO.output(self.PIN_PWM_LEFT, GPIO.LOW) 

        # Cleanup PINs for motor right
        GPIO.output(self.PIN_1_RIGHT, GPIO.LOW)
        GPIO.output(self.PIN_2_RIGHT, GPIO.LOW)
        GPIO.output(self.PIN_PWM_RIGHT, GPIO.LOW)

        GPIO.output(self.PIN_RELAY, GPIO.HIGH)

        time.sleep(1)
        GPIO.cleanup()
        print '[PINS] Done!'
 