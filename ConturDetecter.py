import numpy as np
import cv2 as cv

class ConturDetecter:
    
    def __init__(self):
        self.image = None
        self.contourCenterX = 0
        self.e = 0
        self.MainContour = None
        
    def Process(self):
        imgray = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
        ret, thresh = cv.threshold(imgray,100,255,cv.THRESH_BINARY_INV) #Get Threshold

        _, self.contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #Get contour
        
        self.prev_MC = self.MainContour
        if self.contours:
            self.MainContour = max(self.contours, key=cv.contourArea)
        
            self.height, self.width  = self.image.shape[:2]

            self.middleX = int(self.width/2) #Get X coordenate of the middle point
            self.middleY = int(self.height/2) #Get Y coordenate of the middle point
            
            self.prev_cX = self.contourCenterX
            if self.getContourCenter(self.MainContour) != 0:
                self.contourCenterX = self.getContourCenter(self.MainContour)[0]
                # if abs(self.prev_cX-self.contourCenterX) > 5:
                #     self.correctMainContour(self.prev_cX)
            else:
                self.contourCenterX = 0
            self.e = self.middleX - self.contourCenterX
            self.dir =  int((self.middleX-self.contourCenterX) * self.getContourExtent(self.MainContour))
            
            cv.drawContours(self.image,self.MainContour,-1,(0,255,0),3) #Draw Contour GREEN
            cv.circle(self.image, (self.contourCenterX, self.middleY), 7, (255,255,255), -1) #Draw dX circle WHITE
            cv.circle(self.image, (self.middleX, self.middleY), 3, (0,0,255), -1) #Draw middle circle RED
            
            font = cv.FONT_HERSHEY_SIMPLEX
            cv.putText(self.image,str(self.e),(self.contourCenterX+20, self.middleY), font, 1,(200,0,200),2,cv.LINE_AA)
            # cv.putText(self.image,str(self.dir),(self.contourCenterX+20, self.middleY-30), font, 1,(200,0,200),2,cv.LINE_AA)
            cv.putText(self.image,"Weight:%.3f"%self.getContourExtent(self.MainContour),(self.contourCenterX+20, self.middleY+35), font, 0.5,(200,0,200),1,cv.LINE_AA)
        
    def getContourCenter(self, contour):
        M = cv.moments(contour)
        
        if M["m00"] == 0:
            return 0
        
        x = int(M["m10"]/M["m00"])
        y = int(M["m01"]/M["m00"])
        
        return [x,y]
        
    def getContourExtent(self, contour):
        area = cv.contourArea(contour)
        x,y,w,h = cv.boundingRect(contour)
        rect_area = w*h
        if rect_area > 0:
            return (float(area)/rect_area)
            
    def Aprox(self, a, b, error):
        if abs(a - b) < error:
            return True
        else:
            return False
            
    