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
def getLinePose(image):
    imgray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    r, thresh = cv.threshold(imgray,100,255,cv.THRESH_BINARY_INV)
    # thresh = cv.adaptiveThreshold(imgray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,13,7)
    _, contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    e=0
    if contours:
        MainContour = max(contours, key=cv.contourArea)
        height, width = image.shape[:2]
        middleX = int(width/2) #Get X coordenate of the middle point
        middleY = int(height/2)

        cv.drawContours(image, MainContour,-1,(0,255,0),3)
        if getContourCenter(MainContour) != 0:
            contourCenterX = getContourCenter(MainContour)[0]
            
        else:
            contourCenterX = 0
        cv.circle(image, (contourCenterX, middleY), 7, (255,255,255), -1)
        cv.circle(image, (middleX, middleY), 3, (0,0,255), -1)
        e = middleX - contourCenterX
    return e

def getLinePoseMulti(im, images, errors, slices):
    height, width = im.shape[:2]
    sl = int(height/slices);
    
    for i in range(slices):
        part = sl*i
        crop_img = im[part:part+sl, 0:width]
        errors.append(getLinePose(crop_img))
        images.append(crop_img)
        # images[i].Process()


while True:
    ret, frame = cam.read()
    # img = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
     #Get Threshold
    #thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,13,7)
    e = []
    images = []
    getLinePoseMulti(frame, images, e, 4)
    print(e)
    cv.imshow('frame', frame)
    # cv.imshow('0', images[0])
    # cv.imshow('1', images[1])
    # cv.imshow('2', images[2])
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv.destroyAllWindows()