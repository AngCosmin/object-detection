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

# loop over the frames from the video stream
direction = -100

while True:
	if direction < -10:
		motors.move_motors(0, 35, "forward")
	elif direction > 10:
		motors.move_motors(35, 0, "forward")				
	else:
		motors.move_motors(35, 35, "forward")	

	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
motors.cleanup_pins()
