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
ap.add_argument("-b", "--blocks", type=int, default=2, help="blocks")
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
# ser.flushOutput()
# EV3_IP = "169.254/.253.86"
# EV3_PORT = 5090

# client = udp_client.SimpleUDPClient(EV3_IP, EV3_PORT)

# time.sleep(1)
# sock.connect(('169.254.253.86', 4090))
# cap = cv.VideoCapture(args["camera"])
# cap = cv.VideoCapture(0)
# cap = WebCam.WebCam(src=0).start()
# cap = WebcamVideoStream(src=0).start()
cap = WebCam.WebCam(src=0)
# vs.stream.stream.
# cv2.

# cap.stream.stream
# cap.stream.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
# vs.stream.stream.set(cv2.CAP_PROP_CONTRAST, 0)
# vs.stream.stream.set(cv2.CAP_PROP_WHITE_BALANCE, 0)
# vs.stream.stream.set(cv2.CAP_PROP, 0)
cap =cap.start()
for i in range(5):
    frame = cap.read()
frame = cap.read()
frame = imutils.resize(frame, width=420)

# frames.put(frame)
# frames.put(frame)
# cap2 = WebCam.WebCam(src=0)
# cap.start()
# cap2.start()
# cap.set(3,160)
# cap.set(4,120)
# cap2.set(3,160)
# cap2.set(4,120)
# frame =[]
time.sleep(2)
est2 = False
est = False
# def predictk(imin):
#     image = imin.copy()
#     # image = imin[0:80, 340:420]
    
#     return {'cross':cross, 'stop':stop, 'left':left, 'forward':forward, 'right':right, 'e':e}
def SignDetect():
    global est, est2, stopEn
    time.sleep(0.5)
    mmmm = load_model(args["model"])
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
            print({'cross':cross, 'stop':stop, 'left':left, 'forward':forward, 'right':right, 'e':e})

# def SignDetect(frame2):
#     global est, est2, stopEn
#     # some intensive computation...
#     hsv = cv.cvtColor(frame2, cv.COLOR_BGR2HSV)
#     lower_blue = np.array([64, 92, 33])
#     upper_blue = np.array([155, 255, 255])
#     lower_red = np.array([176, 38, 38])
#     upper_red = np.array([255, 255, 255])
#     # lower_red2 = np.array([240,80,54])
#     # upper_red2 = np.array([255,255,255])
#     r_mask = cv.inRange(hsv, lower_red, upper_red)
#     b_mask = cv.inRange(hsv, lower_blue, upper_blue)
#     # r2_mask = cv.inRange(hsv, lower_red2, upper_red2)
#     b_mask = cv.medianBlur(b_mask, 3)
#     r_mask = cv.medianBlur(r_mask, 3)
#     # b_mask = cv.medianBlur(b_mask, 3)
#     # r_mask = cv.medianBlur(r_mask, 3)
#     # imgray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
#     # ret, thresh = cv.threshold(imgray,100,255,cv.THRESH_BINARY_INV) #Get Threshold
#     _, contours, _ = cv.findContours(b_mask, cv.RETR_TREE,
#                                      cv.CHAIN_APPROX_SIMPLE)  #Get contour
#     _, r_contours, _ = cv.findContours(r_mask, cv.RETR_TREE,
#                                        cv.CHAIN_APPROX_SIMPLE)
#     # MainContour = max(contours, key=cv.contourArea)
#     ok = []
#     # ok = sorted(ok, key=cv.contourArea)
#     # print(ok)
#     for c in contours:
#         # cv.drawContours(frame,c,-1,(0,255,0),3)
#         approx = cv.approxPolyDP(c, cv.arcLength(c, True) * 0.03, True)
#         area = cv.contourArea(approx)
#         if (area > 500) and (area < 78000) and cv.isContourConvex(approx):
#             ok.append(c)
#             cv.drawContours(frame2, max(ok, key=cv.contourArea), -1,
#                             (255, 255, 0), 3)
#         else:
#             continue

#         # print(approx.size/2)
#         if (approx.size / 2 == 4):
#             x2, y2, w2, h2 = cv.boundingRect(c)
#             print(x2, y2, w2, h2)
#             crop = frame2[y2:y2 + h2, x2:x2 + w2]
#             est = True
#             # cv.imshow('crop_b', crop)
#     ok = []
#     # ok = sorted(ok, key=cv.contourArea)
#     # print(ok)
#     for c in r_contours:
#         # cv.drawContours(frame,c,-1,(0,255,0),3)
#         approx = cv.approxPolyDP(c, cv.arcLength(c, True) * 0.03, True)
#         area = cv.contourArea(approx)
#         if (area > 500) and (area < 78000) and cv.isContourConvex(approx):
#             ok.append(c)
#             cv.drawContours(frame2, max(ok, key=cv.contourArea), -1,
#                             (0, 20, 255), 3)
#         else:
#             continue

#         # print(approx.size/2)
#         if (approx.size / 2 > 2):
#             x2, y2, w2, h2 = cv.boundingRect(c)
#             print(x2, y2, w2, h2)
#             crop = frame2[y2:y2 + h2, x2:x2 + w2]

#             est2 = stopEn
#             # cv.imshow('crop_r', crop)
#     cv2.imshow('fr2', frame2)
#     cv2.imshow('th', r_mask)
# def SignDetecter(fr):
#     global cv
#     while True:
#         # frame2 = cap.read()
#         # ret, frame = cap.read()
#         # frames.put(frame)
#         frame2 = fr.get()
#         # frame2 = frame.copy()

#         # time.sleep(0.001)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             qwe = 0
#             break
#         # cv.imshow('o', frame2)
#         # cv.imshow('thresh', b_mask)
#         # cv.imshow('sign_frame', frame2)
# # frame = []
# # cap = cv.VideoCapture(args["camera"])


def send_message(cmd, body):
    if args['serialOn'] == 1:
        global ser
        mes = "#" + cmd + "#" + str(body) + "#" + cmd + "e#\n"
        ser.write(mes.encode('utf-8'))


# cap = WebcamVideoStream(src=args["camera"]).start()
# def data_to_send(err):
# global e, m0_speed, m1_speed, prev_e, motor_r, itg, SP_SPEED
# return str(m0_speed) + '@' + str(m1_speed) + '@' + str(motor_r) + '@' + str(err)

itog = 0
t = 0
ui = False
t2 = 0
ui2 = False


def send_data():
    global e, servo, speed, prev_e, motor_r, itg, qwe, prev_e_itog, itog, est, ui, t, ui2, t2, est2, stopEn
    while qwe:
        # print(e)
        # e_abs = map(abs, e)
        # e_now = (e[0] + e[1] + e[2] + e[3]) / 4
        # p = e_now
        # d = e_now - prev_e
        # itg = itg + e_now
        # pid = p*0.3 + d*2
        # e_itog = e[0] * 0.35 + e[1] * 0.35 + e[2] * 0.2 + e[3] * 0
        e_itog = e[0] * 0.55 + e[1] * 0.45
        d = e_itog - prev_e_itog
        # itg = itg + e_itog
        itog = e_itog * 0.45 + d * 0.95

        prev_e_itog = e_itog
        # print('itog', itog)
        # m0_speed = SP_SPEED + itog
        # m1_speed = SP_SPEED - itog
        prev_e = e
        # sock.send(data_to_send(e_now).encode('utf-8'))
        servo = 90 - itog

        @delay(6.0)
        def stop_on():
            global stopEn
            stopEn = True
            print('st_on')
            # @delay(2.0)
            # def speed_on():
            # speed = 15
            # stopEn = True
            # print('s_on')
            # ui2 = False
            # stop_on()

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
        send_message("s", servo)
        # else:
        # speed = 0
        print(speed, stopEn)
        send_message("m", speed)

        time.sleep(0.08)
        # send_message("/m1", m1_speed)
        # time.sleep(0.02)


time.sleep(1)
send_message("m", 0)
time.sleep(0.02)

# p1 = Process(target=SignDetecter, args=(frames,))
# p1.daemon = True
# p1 = SignDetecter(frames)
# p1.daemon = True
# p1.start()
# p1.join()
# p2 = Process(target=SignDetecter, args=(frames,))
# client.send_message("/m_stop", 0)
# time.sleep(0.02)
t1 = threading.Thread(target=send_data)
t1.daemon = True
t1.start()


# t2 = threading.Thread(target=SignDetecter, args=(frames, ))
# t2.daemon = True
# t2.start()


# if cap.isOpened():  # try to get the first frame
#         ret, frame = cap.read()
#     else:
#         ret = False
# def put_frame(ame):
#     if frames.full():
#         frames.get_nowait()
#     frames.put(ame)
frame = cap.read()
frame = imutils.resize(frame, width=420)

# time.sleep(1)
t2 = threading.Thread(target=SignDetect)
t2.daemon = True
t2.start()
fps = FPS().start()
while True:
    # global frame

    frame3 = cap.read().copy()
    # frame3 = imutils.resize(frame3, width=420)
    # put_frame(frame)
    # SignDetect(frame.copy())
    # frames.put(frame)
    # f2 = frame3[0:80, 340:420]
    # print(predictk(f2.copy()))
    # frame3 = frame.copy()
    # if frame != None:
    h, w = frame3.shape[:2]
    frame3 = frame3[h // 6 * 3:h, w // 10 * 0:w // 10 * 10]
    MultiLines(frame3, Detecters, blocks, 1, e)
    cv.imshow('frame', frame)
    cv.imshow('frame3', frame3)
    # else:
    #     cap = WebcamVideoStream(src=args["camera"]).start()
    fps.update()
    if cv.waitKey(1) & 0xFF == ord('q'):
        speed = 0
        send_message("m", 0)
        qwe = 0
        # p1.stopProcess()
        break
qwe = 0
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# t1._delete()
# send_message("m", 0)
# time.sleep(0.02)
# client.send_message("/m_stop", 0)
# time.sleep(0.02)
cap.stop()
# p1.stopProcess()
# cap2.stop()
# cap.release()
# cap2.release()
# cap.stop()
cv.destroyAllWindows()