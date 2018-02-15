#!/usr/bin/env python

# import the necessary packages
from imutils.video import VideoStream
from collections import deque
from classes.MotorsController import MotorsController
from classes.Servo import Servo
from classes.ServoNew import ServoNew
from classes.Relay import Relay
import datetime
import argparse
import imutils
import time
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())
 
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(1.0)

greenLower = (21, 100, 50)
greenUpper = (41, 255, 255)

pts = deque(maxlen=args["buffer"])

lastY = ''
width = 400
height = 300

motors = MotorsController()

# Turn on motors
relay = Relay()
relay.turn_on()

# Servo
servo = ServoNew()
servoValue = 1500;
servo.change(servoValue)

lastDirection = "none"

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=width)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			horizontaly_object_position = int(x) - width / 2
			verticaly_object_position = int(y) - height / 2

			if lastY == '':
				lastY = verticaly_object_position

			# write center coords on the screen
			text = " X: " +  str(int(x)) + " Y: " + str(int(y)) + " HORIZ: " + str(horizontaly_object_position)

			# if horizontaly_object_position > 15:
			# 	# Object on the right side of the image

			# 	object_position_percentage = float(horizontaly_object_position) / (width / 2) * 100

			# 	if object_position_percentage <= 50:
			# 		if object_position_percentage < 7.5:
			# 			object_position_percentage = 7.5

			# 		text += " LEFT " + str(object_position_percentage * 2) + " RIGHT 0"
			# 		motors.move_motors(object_position_percentage * 2, 0)	
			# 	else:
			# 		if object_position_percentage - 50 < 7.5:
			# 			object_position_percentage = 50 + 7.5

			# 		text += " LEFT 100 RIGHT " + str(-(object_position_percentage - 50) * 2)
			# 		motors.move_motors(100, -(object_position_percentage - 50) * 2)	
			# elif horizontaly_object_position < -15:
			# 	object_position_percentage = -float(horizontaly_object_position) / (width / 2) * 100

			# 	if object_position_percentage <= 50:
			# 		if object_position_percentage < 7.5:
			# 			object_position_percentage = 7.5

			# 		text += " LEFT 0 RIGHT " + str(object_position_percentage * 2)  
			# 		motors.move_motors(0, object_position_percentage * 2)	
			# 	else:
			# 		if object_position_percentage - 50 < 7.5:
			# 			object_position_percentage = 50 + 7.5
						
			# 		text += " LEFT " + str(-(object_position_percentage - 50) * 2) + " RIGHT 100"
			# 		motors.move_motors(-(object_position_percentage - 50) * 2, 100)
			# else:
			# 	text += "LEFT 30 RIGHT 30"
			# 	motors.move_motors(100, 100)

			if abs(lastY - verticaly_object_position) > 20:
				if verticaly_object_position - lastY < 0:
					servoValue = servoValue - abs(lastY - verticaly_object_position) * 1000 / height

					if servoValue > 2000:
						servoValue = 2000

					if servoValue < 1000:
						servoValue = 1000
					
					# servo.change(servoValue)
				else:
					servoValue = servoValue + abs(lastY - verticaly_object_position) * 1000 / height				

					if servoValue > 2000:
						servoValue = 2000

					if servoValue < 1000:
						servoValue = 1000

					# servo.change(servoValue)
				lastY = verticaly_object_position

			text += "Servo value: " + str(servoValue) + " Y: " + str(verticaly_object_position)

			cv2.putText(frame, text, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1) #Draw the text
	else:
		motors.stop()

	# show the frame
	cv2.imshow("Frame", frame)    
	cv2.imshow("Mask", mask)
	
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
 
# do a bit of cleanup
relay.turn_off()
servo.clean()
motors.clean()

cv2.destroyAllWindows()
vs.stop()
