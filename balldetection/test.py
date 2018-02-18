#!/usr/bin/env python

from imutils.video import VideoStream
import imutils
import cv2
import sys
import time
import numpy as np

colorLower = (29, 86, 6)
colorUpper = (64, 255, 255)

camera = VideoStream(usePiCamera=True)
camera.start()

time.sleep(1)

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

while True:
    frame = camera.read()

    frame = adjust_gamma(frame, gamma=1.5)

    # Resize frame
    frame = imutils.resize(frame, width=300)

    # Apply median filter
    frame = cv2.medianBlur(frame, 5)

    # Convert image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # bright_red_lower_bounds = (0, 100, 100)
    # bright_red_upper_bounds = (10, 255, 255)
    # bright_red_mask = cv2.inRange(hsv, bright_red_lower_bounds, bright_red_upper_bounds)

    # dark_red_lower_bounds = (160, 100, 100)
    # dark_red_upper_bounds = (179, 255, 255)
    # dark_red_mask = cv2.inRange(hsv, dark_red_lower_bounds, dark_red_upper_bounds)

    # after masking the red shades out, I add the two images 
    # mask = cv2.addWeighted(bright_red_mask, 1.0, dark_red_mask, 1.0, 0.0)

    # Get pieces within the color range
    mask = cv2.inRange(hsv, colorLower, colorUpper)

    # Erodate to eliminate noise
    mask = cv2.erode(mask, None, iterations=2)

    # Dilatate
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contour
    contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    # If contour was found
    if len(contour) > 0:
        # Find the largest contour in the mask
        circle = max(contour, key=cv2.contourArea)

        #  Use contour to compute the minimum enclosing circle
        ((x, y), radius) = cv2.minEnclosingCircle(circle)

        M = cv2.moments(circle)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            # draw the circle and centroid on the frame,
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    cv2.imshow("Frame", frame)    
    cv2.imshow("Mask", mask) 

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break	