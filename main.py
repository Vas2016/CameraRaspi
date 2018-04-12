import numpy as np
import cv2 as cv
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--camera", type=int, default=0,
	help="camera")
args = vars(ap.parse_args())

cam = cv.VideoCapture(args["camera"])

def getContourCenter(contour):
    M = cv.moments(contour)
        
    if M["m00"] == 0:
        return 0
        
    x = int(M["m10"]/M["m00"])
    y = int(M["m01"]/M["m00"])
        
    return [x,y]

while True:
    ret, frame = cam.read()
    img = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
    r, thresh = cv.threshold(img,100,255,cv.THRESH_BINARY_INV) #Get Threshold
    #thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,13,7)
    _, contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    if contours:
        MainContour = max(contours, key=cv.contourArea)
        height, width = frame.shape[:2]
        middleX = int(width/2) #Get X coordenate of the middle point
        middleY = int(height/2)
        cv.drawContours(frame, MainContour,-1,(0,255,0),3)
        if getContourCenter(MainContour) != 0:
            contourCenterX = getContourCenter(MainContour)[0]
            
        else:
            contourCenterX = 0
        cv.circle(frame, (contourCenterX, middleY), 7, (255,255,255), -1)
        cv.circle(frame, (middleX, middleY), 3, (0,0,255), -1)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()