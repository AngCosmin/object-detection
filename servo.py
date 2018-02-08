#!/usr/bin/env python

from classes.motors import Motors
from classes.servo import Servo

try:
    # Turn on motors
    motors = Motors()
    motors.toggleMotors("on")

    servo = Servo()
    while True:
        duty_cycle = float(input("Enter Duty Cycle (Left = 5 to Right = 10):"))
        servo.changeDutyCycle(duty_cycle)

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    servo.cleanup_pins()