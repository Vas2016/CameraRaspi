import numpy as np
import cv2 as cv
import argparse
import threading
import time
import socket
# from imutils.video import VideoStream
from imutils.video import WebcamVideoStream

from ConturDetecter import *
from Utils import *
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0,
	help="camera")
ap.add_argument("-b", "--blocks", type=int, default=4,
	help="camera")
args = vars(ap.parse_args())

sock = socket.socket()

complited = False
frame = None
Detecters=[]
blocks = args["blocks"]
for q in range(blocks):
    Detecters.append(ConturDetecter())
e = []
for q in range(blocks):
    e.append(0)
sock.connect(('169.254.253.86', 4090))
# cam = cv.VideoCapture(args["camera"])

cap = WebcamVideoStream(src=args["camera"]).start()

def send_data():
    global e
    while True:
        print(e)
        # e_abs = map(abs, e)
        e_sent = (e[0] + e[1] + e[2] + e[3]) / 4
        sock.send(str(str(float(e_sent)) + '@1').encode('utf-8'))
        time.sleep(0.08)

t1 = threading.Thread(target=send_data)
t1.daemon = True
t1.start()
time.sleep(1)



while True:
    # ret, frame = cam.read()
    frame = cap.read()
    MultiLines(frame, Detecters, blocks, e)
    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# cam.release()
cv.destroyAllWindows()