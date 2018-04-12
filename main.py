import numpy as np
import cv2 as cv
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0,
	help="camera")
args = vars(ap.parse_args())

cam = cv.VideoCapture(args["camera"])

while True:
    ret, frame = cam.read()
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()