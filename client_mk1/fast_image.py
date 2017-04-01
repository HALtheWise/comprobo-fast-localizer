import cv2
import numpy as np

class Image(object):
    def __init__(self, img):
        self.img = img
        self.pixelsAccessed = []

    def getHSV(self, x, y):
        x = int(x)
        y = int(y)
        self.pixelsAccessed.append((x, y))
        rgb = self.img[y:y + 1, x:x + 1]
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

        if hsv is None:
            raise IndexError

        return hsv[0, 0]

    def draw(self, img):
        color = (0, 0, 255)
        for p in self.pixelsAccessed:
            img[p[1], p[0]] = color

