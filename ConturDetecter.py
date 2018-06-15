import numpy as np
import cv2 as cv

class ConturDetecter:
    
    def __init__(self):
        self.image = None
        self.contourCenterX = 0
        self.e = 0
        self.MainContour = None

    def getCorrect(self, conturs, direct, w, h):
        x = 0
        min1 = 1000
        cx = []
        pre_x = 0
        pre_y = 0
        if len(conturs)>0:
            for i in conturs:
                if(i is not None):
                    area = cv.contourArea(i)
                    if self.getContourCenter(i) != 0:
                        pre_x = self.getContourCenter(i)[0]
                        pre_y = self.getContourCenter(i)[1]
                        # pre_x = pre[0]
                        #  = pre[1]
                        if(area>=250) and (pre_x < w/15*14) and (pre_y > h/10*9):
                            # M = cv.moments(i)
                            
                            
                            if(direct == 0):
                                if(abs(pre_x-w/2)<min1):
                                    min1 = abs(pre_x-w/2)
                                    x = w/2 - pre_x
                                    cx.append(pre_x)
                            elif(direct > 0):
                                if(abs(pre_x-w)<min1):
                                    min1 = abs(pre_x-w)
                                    x = w/2 - pre_x
                                    cx.append(pre_x)
                            elif(direct < 0):
                                if(pre_x<min1):
                                    min1 = pre_x
                                    x = w/2 - pre_x
                                    cx.append(pre_x)
        return cx
    
    def getContourCenterX22(self, c):
        M = cv.moments(c)
        a  = cv.contourArea(c)
        x2,y2,w2,h2 = cv.boundingRect(c)
       
        if (M["m00"] == 0) or (a < 200) or (w2/h2 > 1.8):
            return 70000
        else:
            x = int(M["m10"]/M["m00"])
            # x = int(M["m10"]/M["m00"])
            # y = int(M["m01"]/M["m00"])
            # y = int(M["m01"]/M["m00"])
            # print(abs(x-self.width))
            return abs(x-self.width/2)
    # def 
    # def 
    def Process(self, cCount, direct):
        imgray = cv.cvtColor(self.image,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
        imgray = cv.medianBlur(imgray, 5)
        ret, thresh = cv.threshold(imgray,100,255,cv.THRESH_BINARY_INV) #Get Threshold
        # cv.imshow('thr', thresh)
        # imgray = cv.cvtColor(self.image,cv.COLOR_BGR2HSV)
        # thresh = cv.inRange(imgray, (0, 0, 0), (150, 255, 128))
        # ret, thresh = cv.threshold(imgray,)
        # cv.adaptiveThreshold()
        # thresh = cv.adaptiveThreshold(imgray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            # cv.THRESH_BINARY_INV,11,2)
        # thresh = cv.invert(thresh)
        _, self.contours, _ = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #Get contour
        
        if cCount == 1:
            self.prev_MC = self.MainContour
            self.height, self.width  = self.image.shape[:2]
            # cx = self.getCorrect(self.contours, direct, self.width, self.height)
            # print(cx)
            # cx = []
            
            # self.contours = 
            if self.contours:
                self.contours = sorted(self.contours, key=cv.contourArea, reverse=True)[:5]
                # for i in self.contours:
                    # M = cv.moments(i)
                    # if M["m00"] != 0:
                # pre_x = int(M["m10"]/M["m00"])
                if direct== -1:
                    self.contours = sorted(self.contours, key=self.getContourCenterX)
                elif direct== 1:
                    self.contours = sorted(self.contours, key=self.getContourCenterX, reverse=True)
                else:
                    self.contours = sorted(self.contours, key=self.getContourCenterX22)
                    # self.contours[1] 
                    # self.contours = sorted(self.contours, key=self.getContourCenterX)
                    # /
                    # self.contours = sorted(self.contours, key=self.getContourCenterX)
                        # elif direct== 0:
                        #     # pre_x = self.getContourCenter(self.MainContour)[0]
                        #     if pre_x < self.width /3*2 and pre_x > self.width /3*1:
                        #         cx.append(i)
                        # else:
                        #     cx.append(i)
            # self.contours=cx
            if self.contours:
                self.MainContour = self.contours[0]
                # for c in self.MainContour:

                

                self.middleX = int(self.width/2) #Get X coordenate of the middle point
                self.middleY = int(self.height/2) #Get Y coordenate of the middle point
                
                self.prev_cX = self.contourCenterX
                p = self.getContourCenter(self.MainContour)
                if p != 0:
                    self.contourCenterX = p[0]
                    x2,y2,w2,h2 = cv.boundingRect(self.MainContour)
                    # if w2 > (self.width // 2):
                    #     if -(self.middleX - self.contourCenterX) >= 0:
                    #         self.contourCenterX += int(w2 * 0.4)
                    #     else:
                    #         self.contourCenterX -= int(w2 * 0.5)
                    # if abs(self.prev_cX-self.contourCenterX) > 5:
                    #     self.correctMainContour(self.prev_cX)
                else:
                    self.contourCenterX = 0
                # self.contourCenterX = 
                self.e = -(self.middleX - self.contourCenterX) / ((self.width - self.middleX) / 100)
                # self.e =  int((self.middleX-self.contourCenterX) * self.getContourExtent(self.MainContour))
                
                cv.drawContours(self.image,self.MainContour,-1,(0,255,0),3) #Draw Contour GREEN
                cv.circle(self.image, (self.contourCenterX, self.middleY), 7, (255,255,255), -1) #Draw dX circle WHITE
                cv.circle(self.image, (self.middleX, self.middleY), 3, (0,0,255), -1) #Draw middle circle RED
                
                font = cv.FONT_HERSHEY_SIMPLEX
                cv.putText(self.image,str(self.e),(self.contourCenterX+20, self.middleY), font, 1,(200,0,200),2,cv.LINE_AA)
                # cv.putText(self.image,str(self.dir),(self.contourCenterX+20, self.middleY-30), font, 1,(200,0,200),2,cv.LINE_AA)
                cv.putText(self.image,"Weight:%.3f"%cv.contourArea(self.MainContour),(self.contourCenterX+20, self.middleY+35), font, 0.5,(200,0,200),1,cv.LINE_AA)
                # cv.putText(self.image,"Weight:%.3f"%self.getContourExtent(self.MainContour),(self.contourCenterX+20, self.middleY+35), font, 0.5,(200,0,200),1,cv.LINE_AA)
            # else:
        elif cCount > 1:
            if self.contours:
                self.MainContours = sorted(self.contours, key=cv.contourArea, reverse=True)[0:cCount]
            
                self.height, self.width  = self.image.shape[:2]

                self.middleX = int(self.width/2) #Get X coordenate of the middle point
                self.middleY = int(self.height/2) #Get Y coordenate of the middle point
                cv.circle(self.image, (self.middleX, self.middleY), 3, (0,0,255), -1)
                font = cv.FONT_HERSHEY_SIMPLEX
                # self.contoursCentreX = []
                self.mean_e = 0
                self.mean_c = 0
                self.prev_cX = 0
                self.prev_e = 0
                self.prev_w = 0
                self.turn = 0
                self.wc = 0
                for mc in self.MainContours:
                    # mc = self.MainContours[i]
                    self.prev_cX = self.contourCenterX
                    if self.getContourCenter(mc) != 0:
                        self.contourCenterX = self.getContourCenter(mc)[0]
                        self.prev_w = self.wc
                        x2,y2,w2,h2 = cv.boundingRect(mc)
                        self.wc = w2
                            # if w2 > (self.width / 2):
                            #     if (self.middleX - self.contourCenterX) >= 0:
                            #         self.contourCenterX -= int(w2 * 0.4)
                            #     else:
                            #         self.contourCenterX += int(w2 * 0.4)
                        
                        # if abs(self.prev_cX-self.contourCenterX) > 5:
                            
                        #     self.correctMainContour(self.prev_cX)
                    else:
                        self.contourCenterX = 0
                    self.prev_e = self.e
                    self.e = -(self.middleX - self.contourCenterX) / ((self.width - self.middleX) / 100)
                    # if (self.wc - self.prev_w) > 10:
                    
                    #     # if abs(self.prev_e) < abs(self.e):
                    #     # print('oo', self.wc - self.prev_w)
                    #     if self.e >= 0:
                    #         turn = 1
                    #     else:
                    #         turn = -1
                    # else:
                    #     turn = 0
                    # elif (self.wc - self.prev_w) < 20:
                    #     if self.prev_e >= 0:
                    #         turn = 1
                    #     else:
                    #         turn = 0
                    self.mean_e += self.e
                    self.mean_c += self.contourCenterX
                    # self.e =  int((self.middleX-self.contourCenterX) * self.getContourExtent(self.MainContour))

                    cv.drawContours(self.image,mc,-1,(0,255,0),3) #Draw Contour GREEN
                    cv.circle(self.image, (self.contourCenterX, self.middleY), 7, (255,255,255), -1) #Draw dX circle WHITE
                    #Draw middle circle RED
                    # cv.putText(self.image,str(self.e),(self.contourCenterX+20, self.middleY), font, 1,(200,0,200),2,cv.LINE_AA)
                    # cv.putText(self.image,str(self.dir),(self.contourCenterX+20, self.middleY-30), font, 1,(200,0,200),2,cv.LINE_AA)
                    # cv.putText(self.image,"Weight:%.3f"%self.getContourExtent(self.MainContour),(self.contourCenterX+20, self.middleY+35), font, 0.5,(200,0,200),1,cv.LINE_AA)
                
                # self.maxW
                # self.turn   
                self.e = self.mean_e / cCount
                self.contourCenterX = int(self.mean_c / cCount)
                cv.circle(self.image, (self.contourCenterX, self.middleY), 7, (0,255,180), -1) #Draw dX circle WHITE
                cv.putText(self.image,str(self.turn),(5, 100), font, 0.5,(200,0,200),1,cv.LINE_AA)
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
            
    