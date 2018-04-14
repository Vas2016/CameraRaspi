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
m0_speed = 0
m1_speed = 0
motor_r = 1
prev_e = 0
itg = 0
SP_SPEED = 40
sock.connect(('169.254.253.86', 4090))
# cam = cv.VideoCapture(args["camera"])

cap = WebcamVideoStream(src=args["camera"]).start()
def data_to_send(err):
    global e, m0_speed, m1_speed, prev_e, motor_r, itg, SP_SPEED
    return str(m0_speed) + '@' + str(m1_speed) + '@' + str(motor_r) + '@' + str(err)
def send_data():
    global e, m0_speed, m1_speed, prev_e, motor_r, itg, SP_SPEED
    while True:
        # print(e)
        # e_abs = map(abs, e)
        e_now = (e[0] + e[1] + e[2] + e[3]) / 4
        p = e_now
        d = e_now - prev_e
        itg = itg + e_now
        pid = p*0.5 + d*10
        print('pid', pid)
        m0_speed = SP_SPEED + pid
        m1_speed = SP_SPEED - pid
        prev_e = e_now
        sock.send(data_to_send(e_now).encode('utf-8'))
        time.sleep(0.02)

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