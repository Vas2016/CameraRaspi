import numpy as np
import cv2 as cv
import argparse
import threading
from multiprocessing import Process, Queue
import time
import socket
import serial
import WebCam
# import SignKeras

from imutils.video import VideoStream
import imutils
from imutils.video import FPS
# import random
# rando
# from imutils.video import VideoStream
# from imutils.video import WebcamVideoStream

from ConturDetecter import *
from Utils import *

stopEn = True
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0, help="camera")
ap.add_argument("-b", "--blocks", type=int, default=1, help="blocks")
ap.add_argument(
    "-s", "--serial", type=str, default="/dev/ttyACM0", help="serial")
ap.add_argument("-S", "--serialOn", type=int, default=1, help="serialOn")
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
args = vars(ap.parse_args())
# frames = Queue()
# sock = socket.socket()
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
# import cv2
# import numpy as np


complited = False
# frame = None
Detecters = []
blocks = args["blocks"]
for q in range(blocks):
    Detecters.append(ConturDetecter())
e = []
for q in range(blocks):
    e.append(0)
speed = 15
servo = 0
motor_r = 1
prev_e = []
itg = 0
SP_SPEED = 30
prev_e_itog = 0
if args['serialOn'] == 1:
    ser = serial.Serial(args["serial"], 115200)
    # ser.open()
    ser.flushInput()
qwe = True
#
cap = WebCam.WebCam(src=0)
cap =cap.start()
for i in range(5):
    frame = cap.read()
frame = cap.read()
frame = imutils.resize(frame, width=420)

time.sleep(2)
est2 = False
est = False
direct = 0
signs = {'cross':0, 'stop':0, 'left':0, 'forward':0, 'right':0, 'e':0}

def maxIndex(a):
    m  = "e"
    for i in a:
        if a[i] > a[m]:
            m = i
    return m
sign_direct = True
def SignDetect():
    global est, est2, stopEn, signs, direct, sign_direct
    time.sleep(0.5)
    mmmm = load_model(args["model"])
    @delay(6.0)
    def on_direct_sign():
        global sign_direct
        sign_direct = True
    while qwe:
        frame2 = cap.read().copy()
        # frame2 = cap.read()
        # frame2 = imutils.resize(frame2, width=420)
        if frame2 is not None:
            image = frame2[0:80, 340:420]
            image = cv.resize(image, (38, 38))
            # cv2.imshow("toNet", image)
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            (cross, stop, left, forward, right, e) = mmmm.predict(image)[0]
            # K.clear_session()
            now_pre = {'cross':cross, 'stop':stop, 'left':left, 'forward':forward, 'right':right, 'e':e}
            # for e in now_pre:
            # print(maxIndex(now_pre))
            signs[maxIndex(now_pre)]+=1
            
            if signs[maxIndex(signs)] > 50:
                if sign_direct == True:
                    if maxIndex(now_pre) == 'left':
                        # if direct == 0:
                        servo = 90-25
                        # sign_direct = False
                        # on_direct_sign()
                    elif maxIndex(now_pre) == 'right':
                        # if direct == 0:
                        servo = 90+25
                        # sign_direct = False
                        # on_direct_sign()
                    elif maxIndex(now_pre) == 'forward':
                        # if direct == 0:
                        servo = 90
                        # sign_direct = False
                        # on_direct_sign()
                    else:
                        servo = 90
                now_pre = {'cross':0, 'stop':0, 'left':0, 'forward':0, 'right':0, 'e':0}


def send_message(cmd, body):
    if args['serialOn'] == 1:
        global ser
        mes = "#" + cmd + "#" + str(body) + "#" + cmd + "e#\n"
        ser.write(mes.encode('utf-8'))


itog = 0
t = 0
ui = False
t2 = 0
ui2 = False


def send_data():
    global e, servo, speed, prev_e, motor_r, itg, qwe, prev_e_itog, itog, est, ui, t, ui2, t2, est2, stopEn
    @delay(6.0)
    def stop_on():
        global stopEn
        stopEn = True
        print('st_on')
    while qwe:
        # e_itog = e[0] * 0.55 + e[1] * 0.45
        # e_itog = e[0]
        # d = e_itog - prev_e_itog
        # itg = itg + e_itog
        # itog = e_itog * 0.56 + d * 1.2
        # itog = e_itog * 0.58 + d * 1.3
        # itog = 
        # prev_e_itog = e_itog
        # print('itog', itog)
        # m0_speed = SP_SPEED + itog
        # m1_speed = SP_SPEED - itog
        # prev_e = e
        # sock.send(data_to_send(e_now).encode('utf-8'))
        # servo = 90 - itog
            # if stopEn == True:
        if est2 == True:
            speed = 0
            send_message("m", speed)
            time.sleep(0.08)
            send_message("m", speed)
            time.sleep(0.08)
            send_message("m", speed)
            time.sleep(0.08)
            send_message("m", speed)
            time.sleep(0.08)
            send_message("m", speed)
            # speed_on()
            est2 = False  # t2 = 0
            # ui2 = True
            stopEn = False
            time.sleep(2.5)
            speed = 15
            stop_on()

        # if ui2 == False:
        #     # else:
        if est == True:
            speed = 7
            est = False
            t = 0
            ui = True
        if ui == True:
            t+=1
            speed = 7
            if t > 100:
                ui = False
        else:
            speed = 15
        send_message("s", int(servo))
        # else:
        # speed = 0
        print(speed, servo, direct)
        send_message("m", int(speed))

        # time.sleep(0.08)
        # send_message("/m1", m1_speed)
        time.sleep(0.05)


time.sleep(1)
send_message("m", 0)
time.sleep(0.02)


t1 = threading.Thread(target=send_data)
t1.daemon = True
t1.start()



frame = cap.read()
frame = imutils.resize(frame, width=420)

# time.sleep(1)
t2 = threading.Thread(target=SignDetect)
t2.daemon = True
t2.start()
fps = FPS().start()
while True:
    # global frame

    # frame3 = cap.read().copy()

    # h, w = frame3.shape[:2]
    # print(direct)
    # frame3 = frame3[h // 6 * 3:h, w // 10 * 0:w // 10 * 10]
    # MultiLines(frame3, Detecters, blocks, 1, e, 0)
    cv.imshow('frame', cap.read())
    # cv.imshow('frame3', frame3)
    
    # else:
    #     cap = WebcamVideoStream(src=args["camera"]).start()
    fps.update()
    if cv.waitKey(1) & 0xFF == ord('q'):
        speed = 0
        send_message("m", 0)
        qwe = 0
        # p1.stopProcess()
        break
qwe = False
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
send_message("m", 0)

cap.stop()
cv.destroyAllWindows()