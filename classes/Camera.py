from imutils.video import VideoStream
import imutils

class Camera:
    def __init__(self, usePiCamera=True):
        self.camera = VideoStream(usePiCamera).start()

    def read(self):
        return self.camera.read()

    def stop(self):
        self.camera.stop()

    def resize(self, frame, width=400):
        return imutils.resize(frame, width=width)