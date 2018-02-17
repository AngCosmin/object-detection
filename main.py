#!/usr/bin/env python

from imutils.video import VideoStream
from classes.MotorsController import MotorsController
from classes.ServoController import ServoController
from classes.RelayController import RelayController
from classes.Camera import Camera
from time import sleep
from time import time
import RPi.GPIO as GPIO
import ConfigParser
import sys
import cv2



def read_config():
	config = ConfigParser.RawConfigParser()

	try:
		config.read('./config.cfg')
		width = config.getint('Image', 'width')
		height = config.getint('Image', 'height')

		colorLowerH = config.getint('ColorLower', 'H')
		colorLowerS = config.getint('ColorLower', 'S')
		colorLowerV = config.getint('ColorLower', 'V')

		colorUpperH = config.getint('ColorUpper', 'H')
		colorUpperS = config.getint('ColorUpper', 'S')
		colorUpperV = config.getint('ColorUpper', 'V')

		colorLower = (colorLowerH, colorLowerS, colorLowerV)
		colorUpper = (colorUpperH, colorUpperS, colorUpperV)

		return width, height, colorLower, colorUpper
	except Exception as e:
		print e

def clean():
	motors.clean()
	relay.clean()
	servo.clean()
	camera.clean()
	GPIO.cleanup()

if __name__ == "__main__":
	width, height, colorLower, colorUpper = read_config()

	camera = Camera(colorLower, colorUpper)
	motors = MotorsController()
	relay = RelayController()
	servo = ServoController()

	relay.start()

	try: 
		while True:
			frame, mask, x, y = camera.compute()

			if x != sys.maxint and y != sys.maxint:
				object_x = x - width / 2
				object_y = y - height / 2

				# Update the last active time
				lastActiveTime = time()

				# Activate motors
				# motors.go_to_object(object_x)

				# Activate servo
				servo.compute(object_y)
			else:
				motors.randomly_activate()

			# show the frame
			cv2.imshow("Frame", frame)    
			cv2.imshow("Mask", mask)
			
			key = cv2.waitKey(1) & 0xFF

			if key == ord("q"):
				clean()
				break		

	except Exception as e: 
		print e
		clean()