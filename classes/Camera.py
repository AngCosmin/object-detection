from imutils.video import VideoStream
import imutils
import cv2
import sys

class Camera:
    def __init__(self, colorLower, colorUpper, usePiCamera=True):
        self.colorLower = colorLower
        self.colorUpper = colorUpper
        self.camera = VideoStream(usePiCamera=usePiCamera)
        self.camera.start()

    def compute(self):
        try: 
            frame = None
            mask = None
            x = sys.maxint
            y = sys.maxint

            frame = self.camera.read()

            # Resize frame
            frame = imutils.resize(frame, width=400)

            # Convert image to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Get pieces within the color range
            mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)

            # Apply gaussian blur
            mask = cv2.GaussianBlur(mask, (5,5),0)

            # Erodate to eliminate noise
            mask = cv2.erode(mask, None, iterations=2)

            # Dilatate
            mask = cv2.dilate(mask, None, iterations=2)

            # Find contour
            contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            
            # If contour was found
            if len(contour) > 0:
                # find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid

                circle = max(contour, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(circle)
                M = cv2.moments(circle)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                print str(x) + " " + str(y)        

                if radius > 7:
                    # draw the circle and centroid on the frame,
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

                    if frame == None:
                        print 'Frame none'
                    if mask == None:
                        print 'Mask none'

                    return frame, mask, x, y
            else:
                if frame == None:
                    print 'Frame none'
                if mask == None:
                    print 'Mask none'
                if x == None:
                    print 'x none'
                if y == None:
                    print 'y none'

                return frame, mask, x, y
        except Exception as e:
            print e

    def clean(self):
        self.camera.stop() 
        cv2.destroyAllWindows()