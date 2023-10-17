'''
Camera Classifier v0.1 Alpha
Copyright (c) NeuralNine

Instagram: @neuralnine
YouTube: NeuralNine
Website: www.neuralnine.com
'''

import cv2 as cv

class Camera:

    def __init__(self):
        self.camera = cv.VideoCapture(0) # Wenn Bild schwarz einfach mal den Integer erhöhen. Steht für welche Kamera als Input genutzt wird.
        if not self.camera.isOpened():
            raise ValueError("Unable to open camera!")
        # Setzen Sie die Auflösung auf 1920x1080
        self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
        self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                return (ret,  frame)
            else:
                return (ret, None)
        else:
            return None