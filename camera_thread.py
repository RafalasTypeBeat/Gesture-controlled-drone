import cv2
import threading

class CameraThread(threading.Thread):
    def __init__(self, src=0, width=640, height=480):
        super().__init__()
        self.src = src
        self.width = width
        self.height = height
        self.cap = None
        self.frame = None
        self.running = False

    def run(self):
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
