import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(1)
frame = []

from keras.preprocessing.image import img_to_array
from keras.models import load_model
# import cv
import numpy as np
model = load_model('signs22.keras')
def maxIndex(a):
	m  = "e"
	for i in a:
		if a[i] > a[m]:
			m = i
	return m
def predict(imin):
	global model
	image = imin.copy()
	# image = imin[0:80, 340:420]
	image = cv.resize(image, (38, 38))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	return model.predict(image)[0]
while True:
	# global frame
	ret, frame = cap.read()
	frame = frame
	frq = frame.copy()
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	lower_blue = np.array([50, 30, 33])
	# frame_blue = cv.inRange(hsv, (90, 200, 50), (150, 255, 255))
	upper_blue = np.array([155, 255, 255])
	lower_red = np.array([0,200,0])
	upper_red = np.array([19,255,255])
	# lower_red2 = np.array([240,80,54])
	# upper_red2 = np.array([255,255,255])
	frame_red = cv.inRange(hsv, (50, 50, 70), (90, 90, 255))
	frame_blue = cv.inRange(hsv, lower_blue, upper_blue)
	# # r2_mask = cv.inRange(hsv, lower_red2, upper_red2)
	frame_blue = cv.medianBlur(frame_blue, 5)
	frame_red = cv.medianBlur(frame_red, 7)
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
	cv.imshow('thresh', frame_blue)
	cv.imshow('thresh_red', frame_red)
	_, con, hierarchy = cv.findContours(frame_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	if len(con) > 0:
		cv.drawContours(frame,con,-1,(150,10,255),3)
		# max_con = max(con, key=cv.contourArea)
		con = sorted(con, key=cv.contourArea, reverse=True)
		con = con[0:6]
		for i in range(len(con)):
			# appr = cv.approxPolyDP(con[i], cv.arcLength(con[i], True) * 0.03, True)
			x,y,w,h = cv.boundingRect(con[i])
			# if appr.size == 4:
			# 	cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
			# 	fr2 = frq[y:y+h, x:x+w]
			# 	(cross, stop, left, forward, right, e) = predict(fr2)
			# 	now_pre = {'cross':cross, 'e':e}
			# 	print(maxIndex(now_pre))
			# 	cv.imshow('q2', fr2)
			if len(con[i]) >= 5:
				# ellipse=cv.fitEllipse(contours[0])
				max_con = con[i]
				# for i in range(len(con)):
				# if len(con[i])>len(max_con):
					# max_con = con[i]
				ellipse = cv.fitEllipse(max_con)
				# (x,y),radius = cv.minEnclosingCircle(max_con)

				x1, y1 = ellipse[0]
				x2, y2 = ellipse[1]

				t1 = ((int(x1)-int(x2/2)), (int(y1)-int(y2/2)))
				t2 = ((int(x1)+int(x2/2)), (int(y1)+int(y2/2)))

				# pixel_ellips_blue = abs((int(y1)-int(y2/2))-(int(y1)+int(y2/2)))*0.15 + 0.85 * pixel_ellips_blue
				w = (t2[0] - t1[0])
				h = (t2[1] - t1[1])
				# print(w, h)
				if w > 50 and w < 100 and t1[0] > 1 and t1[1] > 1 and t2[0] > 1 and t2[1] > 1 and w/h <1.6 and w/h >0.6 :
					# if 
					# print(t2[0] - t1[0])
					# if radius > 25 and radius < 70:
					# center = (int(x),int(y))
					# radius = i/nt(radius)
					# cv.circle(frame,center,radius,(0,255,0),2)
					
					cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
					# fr = frame[int(y1):int(y2), int(x1):int(x2)]
					# print(x1, x2, y1, y2)
					# print(t1, t2)
					fr = frq[y:y+h, x:x+w]
					(cross, stop, left, forward, right, e) = predict(fr)
					now_pre = {'cross':cross, 'stop':stop, 'left':left, 'forward':forward, 'right':right, 'e':e}
				   
					print(maxIndex(now_pre))
					 # _, con2, _ = cv.findContours(frame_blue[t1[1]:t2[1], t1[0]:t2[0]], cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
					# h, w = 
					# cv.drawContours(fr,con,-1,(150,10,255),1)
					print(fr.shape[:2])
					
					cv.imshow('q', fr)
				break
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
	
	cv.imshow('frame', frame)
	
	if cv.waitKey(1) & 0xFF == ord('q'):
		qwe = 0
		break

cap.release()
# cap.stop()
cv.destroyAllWindows()