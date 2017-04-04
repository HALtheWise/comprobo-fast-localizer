from __future__ import print_function, division

import numpy as np
import cv2

def get_frames(vpath):
    video = cv2.VideoCapture(vpath) #grab the video
    frames = []
    while True:
        frame = video.read()
        if frame[0]: #If the frame is valid
            frames.append(frame[1])
        else:
            return np.array(frames)

def get_circles(mat):
    gs = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    return cv2.HoughCircles(gs, cv2.cv.CV_HOUGH_GRADIENT, 2, 40)


if __name__ == "__main__":
    imgs = get_frames("./circle1.mp4")
    fst_frame = imgs[0]
    circles = get_circles(fst_frame)
    print(circles)
    while True:
        for i in circles[0, :]:
            cv2.circle(fst_frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(fst_frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        cv2.imshow("first frame", fst_frame)
        cv2.waitKey(10)
