#!/usr/bin/env python

# import the necessary packages
from imutils.video import VideoStream
from collections import deque
from classes.motors import Motors
from classes.servo import Servo
import datetime
import argparse
import imutils
import time
import cv2
 
# Turn on motors
motors = Motors()
motors.toggleMotors("on")

try:
	while True:
		motors.move_motors(100, 100, "forward")
except KeyboardInterrupt:
	motors.cleanup_pins()

 
# do a bit of cleanup
