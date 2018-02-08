#!/usr/bin/env python

from classes.servo import Servo

try:
    servo = Servo()
    while True:
        duty_cycle = float(input("Enter Duty Cycle (Left = 5 to Right = 10):"))
        servo.changeDutyCycle(duty_cycle)

except KeyboardInterrupt:
    print("CTRL-C: Terminating program.")
finally:
    servo.cleanup_pins()