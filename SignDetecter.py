import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
frame = []
while True:
    # global frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([64, 92, 33])
    # frame_blue = cv2.inRange(hsv, (90, 200, 50), (150, 255, 255))
    upper_blue = np.array([155, 255, 255])
    # lower_red = np.array([1,100,80])
    # upper_red = np.array([8,255,255])
    # lower_red2 = np.array([240,80,54])
    # upper_red2 = np.array([255,255,255])
    # r_mask = cv.inRange(hsv, lower_red, upper_red)
    frame_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    # # r2_mask = cv.inRange(hsv, lower_red2, upper_red2)
    frame_blue = cv2.medianBlur(frame_blue, 5)
    # rows = b_mask.shape[0]
    # circles = cv.HoughCircles(b_mask, cv.HOUGH_GRADIENT, 2, rows / 8,
    #                            param1=100, param2=30,
    #                            minRadius=1, maxRadius=300)
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         center = (i[0], i[1])
    #         # circle center
    #         cv.circle(frame, center, 1, (0, 100, 100), 3)
    #         # circle outline
    #         radius = i[2]
    #         cv.circle(frame, center, radius, (255, 0, 255), 3)
    
    # imgray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #Convert to Gray Scale
    # ret, thresh = cv.threshold(imgray,100,255,cv.THRESH_BINARY_INV) #Get Threshold
    # _, contours, _ = cv.findContours(frame_blue,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #Get contour
    # # MainContour = max(contours, key=cv.contourArea)
    # frame_copy = frame_blue.copy()
    cv2.imshow('thresh', frame_blue)
    _, con, hierarchy = cv2.findContours(frame_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(con) > 0:
        cv2.drawContours(frame,con,-1,(150,10,255),3)
        # max_con = max(con, key=cv2.contourArea)
        con = sorted(con, key=cv2.contourArea, reverse=True)
        con = con[0:6]
        for i in range(len(con)):
            if len(con[i]) >= 5:
                # ellipse=cv2.fitEllipse(contours[0])
                max_con = con[i]
                # for i in range(len(con)):
                # if len(con[i])>len(max_con):
                    # max_con = con[i]
                ellipse = cv2.fitEllipse(max_con)

                x1, y1 = ellipse[0]
                x2, y2 = ellipse[1]

                t1 = ((int(x1)-int(x2/2)), (int(y1)-int(y2/2)))
                t2 = ((int(x1)+int(x2/2)), (int(y1)+int(y2/2)))

                # pixel_ellips_blue = abs((int(y1)-int(y2/2))-(int(y1)+int(y2/2)))*0.15 + 0.85 * pixel_ellips_blue
                cv2.rectangle(frame, t1, t2, (0, 255, 100), 3)
    # ok = []
    # ok = sorted(ok, key=cv.contourArea)
    # for c in contours:
    #     # cv.drawContours(frame,c,-1,(0,255,0),3)
    #     approx = cv.approxPolyDP(c, cv.arcLength(c, True)*0.03, True)
    #     area = cv.contourArea(approx)
    #     if (area > 200) and (area < 78000):
    #         ok.append(c)
    #         cv.drawContours(frame,max(ok, key=cv.contourArea),-1,(255,255,0),3)
    #     else:
    #         continue
            
    #     print(approx.size/2)
    #     if (approx.size/2 > 3):
    #         x2,y2,w2,h2 = cv.boundingRect(c)
    #         print(x2, y2, w2, h2)
    #         crop = frame[y2:y2+h2, x2:x2+w2]
    #         cv.imshow('crop', crop)
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        qwe = 0
        break

cap.release()
# cap.stop()
cv2.destroyAllWindows()