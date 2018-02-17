from imutils.video import VideoStream
import imutils
import cv2

class Camera:
    def __init__(self, colorLower, colorUpper, usePiCamera=True):
        self.colorLower = colorLower
        self.colorUpper = colorUpper
        self.camera = VideoStream(usePiCamera=usePiCamera)
        self.camera.start()

    def compute(self):
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

        return frame, mask

    def clean(self):
        cv2.destroyAllWindows()
        self.camera.stop()