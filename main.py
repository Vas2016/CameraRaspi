import numpy as np
import cv2 as cv
import argparse
import threading
import time

from ConturDetecter import *
from Utils import *
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0,
	help="camera")
ap.add_argument("-b", "--blocks", type=int, default=4,
	help="camera")
args = vars(ap.parse_args())


frame = None
Detecters=[]
blocks = args["blocks"]
for q in range(blocks):
    Detecters.append(ConturDetecter())
e = []
for q in range(blocks):
    e.append(0)

cam = cv.VideoCapture(args["camera"])

def getFrame():
    global frame, Detecters, blocks, e
    while (1):
        
        if frame != None: 
            MultiLines(frame, Detecters, blocks, e)
            cv.imshow('frame', frame)
        print(e)

t1 = threading.Thread(target=getFrame)
t1.daemon = True
t1.start()
time.sleep(1)



while True:
    
    # img = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
     #Get Threshold
    #thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,13,7)
    
    # images = []
    # getLinePoseMulti(frame, images, e, 4)
    # 
    ret, frame = cam.read()
    
    # img = RepackImages(Detecters)
    
    cv.imshow('0', frame)
    # cv.imshow('1', images[1])
    # cv.imshow('2', images[2])
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()