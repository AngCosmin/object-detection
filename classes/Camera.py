from imutils.video import VideoStream
import imutils
import cv2

class Camera:
    def __init__(self, usePiCamera=True):
        self.camera = VideoStream(usePiCamera=usePiCamera).start()

    def start(self):
        return self.camera.start()

    def stop(self):
        self.camera.stop()

    def resize(self, frame, width=400):
        return imutils.resize(frame, width=width)