#!/usr/bin/python

import pigpio
import time
from classes.MotorsController import MotorsController

# Turn on motors
motors = MotorsController()
motors.toggleMotors("on")

pi = pigpio.pi()
pi.set_mode(4, pigpio.OUTPUT)

print ("mode: ", pi.get_mode(4))
print("setting to: ",pi.set_servo_pulsewidth(4, 1500))
print("set to: ",pi.get_servo_pulsewidth(4))

time.sleep(1)

print("setting to: ",pi.set_servo_pulsewidth(4, 1000))
print("set to: ",pi.get_servo_pulsewidth(4))

time.sleep(1)

print("setting to: ",pi.set_servo_pulsewidth(4, 2000))
print("set to: ",pi.get_servo_pulsewidth(4))


time.sleep(1)

motors.toggleMotors("off")
pi.stop()