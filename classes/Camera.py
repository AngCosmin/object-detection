from imutils.video import VideoStream
import imutils
import cv2

class Camera:
    def __init__(self, usePiCamera=True):
        self.camera = VideoStream(usePiCamera=usePiCamera)

    def start(self):
        return self.camera.start()

    def stop(self):
        self.camera.stop()

    def resize(self, frame, width=400):
        return imutils.resize(frame, width=width)

    def compute(self, greenLower, greenUpper):
        frame = self.camera.read()

        # Resize frame
        frame = imutils.resize(frame, width=400)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.GaussianBlur(mask, (5,5),0)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        return mask