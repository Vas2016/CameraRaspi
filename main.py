import numpy as np
import cv2 as cv
import argparse
import threading
import time
import socket
import serial

# from imutils.video import VideoStream
# from imutils.video import WebcamVideoStream

from ConturDetecter import *
from Utils import *
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0,
	help="camera")
ap.add_argument("-b", "--blocks", type=int, default=4,
	help="blocks")
ap.add_argument("-s", "--serial", type=str, default="/dev/ttyS0",
	help="serial")
args = vars(ap.parse_args())

# sock = socket.socket()

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
prev_e = []
itg = 0
SP_SPEED = 30
prev_e_itog = 0
ser = serial.Serial(args["serial"], 115200)
# ser.open()
ser.flushInput()
# ser.flushOutput()
# EV3_IP = "169.254/.253.86"
# EV3_PORT = 5090

# client = udp_client.SimpleUDPClient(EV3_IP, EV3_PORT)

# time.sleep(1)
# sock.connect(('169.254.253.86', 4090))
cap = cv.VideoCapture(args["camera"])
def send_message(topic, mes):
    global ser
    ser.write(str(str(topic) + '@' + str(mes) + '@\n').encode('utf-8'))
# cap = WebcamVideoStream(src=args["camera"]).start()
# def data_to_send(err):
    # global e, m0_speed, m1_speed, prev_e, motor_r, itg, SP_SPEED
    # return str(m0_speed) + '@' + str(m1_speed) + '@' + str(motor_r) + '@' + str(err)
qwe = True
def send_data():
    global e, m0_speed, m1_speed, prev_e, motor_r, itg, SP_SPEED, qwe, prev_e_itog
    while qwe:
        print(e)
        # e_abs = map(abs, e)
        # e_now = (e[0] + e[1] + e[2] + e[3]) / 4
        # p = e_now
        # d = e_now - prev_e
        # itg = itg + e_now
        # pid = p*0.3 + d*2
        e_itog = e[0]*0.3 + e[1]*0.35 + e[2]*0.2 + e[3]*0.15
        d = e_itog - prev_e_itog
        itog = e_itog * 0.22 + d * 0.8

        prev_e_itog = e_itog
        print('itog', itog)
        m0_speed = SP_SPEED + itog
        m1_speed = SP_SPEED - itog
        prev_e = e
        # sock.send(data_to_send(e_now).encode('utf-8'))
        
        send_message("/m", str(int(m0_speed)) +'$' + str(int(m1_speed)))
        time.sleep(0.08)
        # send_message("/m1", m1_speed)
        # time.sleep(0.02)
time.sleep(1)
send_message("/m_stop", 1)
time.sleep(0.02)
# client.send_message("/m_stop", 0)
# time.sleep(0.02)
t1 = threading.Thread(target=send_data)
t1.daemon = True
t1.start()

# time.sleep(1)



while True:
    ret, frame = cap.read()
    # frame = cap.read()
    # if frame != None:
    MultiLines(frame, Detecters, blocks, e)
    cv.imshow('frame', frame)
    # else:
    #     cap = WebcamVideoStream(src=args["camera"]).start()
    if cv.waitKey(1) & 0xFF == ord('q'):
        qwe = 0
        break
# t1._delete()
send_message("/m_stop", 0)
time.sleep(0.02)
# client.send_message("/m_stop", 0)
# time.sleep(0.02)
cap.release()
# cap.stop()
cv.destroyAllWindows()