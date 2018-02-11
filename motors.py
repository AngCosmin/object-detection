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

ok = 1

try:
	while True:
		if ok == 1:
			motors.move_motors(0, 5, "forward")
			ok = 0
except KeyboardInterrupt:
	motors.cleanup_pins()

 
# do a bit of cleanup
