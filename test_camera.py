# USAGE
# python test_network.py --model santa_not_santa.model --image images/examples/santa_01.png

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2
from imutils.video import FPS


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to trained model model")
# ap.add_argument("-c", "--camera", required=0,
# 	help="path to input image")
args = vars(ap.parse_args())
model = load_model(args["model"])
# load the image

vs = VideoStream(src=0)
# vs.stream.stream.
# cv2.
vs.stream.stream.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# vs.stream.stream.set(cv2.CAP_PROP_CONTRAST, 0)
# vs.stream.stream.set(cv2.CAP_PROP_WHITE_BALANCE, 0)
# vs.stream.stream.set(cv2.CAP_PROP, 0)
vs = vs.start()
# v
# cv2.Cam
time.sleep(2.0)
i = 0
qq = {'cross':0, 'stop':0, 'left':0, 'forward':0, 'right':0, 'e':0}
fps = FPS().start()
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	image = vs.read()
	image = imutils.resize(image, width=420)
	#image = cv2.imread(args["image"])
	orig = image.copy()
	image = image[0:80, 340:420]
	# pre-process the image for classification
	image = cv2.resize(image, (38, 38))
	cv2.imshow("toNet", image)
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	# load the trained convolutional neural network
	#print("[INFO] loading network...")


	# classify the input image
	(cross, stop, left, forward, right, e) = model.predict(image)[0]
	
	# build the label
	#label = "Orange" if  > notSanta else "Blue"
	#proba = santa if santa > notSanta else notSanta
	w = [cross, stop, left, forward, right, e]
	# print(w)	
	d = ['cross', 'stop', 'left', 'forward', 'right', 'e']
		
	labele = d[w.index(max(w))]

	proba = max(w)
	label = "{}: {:.2f}%".format(labele, proba * 100)
	qq[labele] += 1
	def yy(el):
		return qq[el]
	print(max(qq, key=yy))
	if qq[max(qq, key=yy)] > 70:
		qq = {'cross':0, 'stop':0, 'left':0, 'forward':0, 'right':0, 'e':0}
	# draw the label on the image
	# output = imutils.resize(orig, width=420)
	output = cv2.rectangle(orig, (340, 0), (420, 80), (0, 0, 255))
	cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
		0.7, (0, 255, 0), 2)
	# draw the timestamp on the frame
	

	# show the frame
	cv2.imshow("Frame", output)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	fps.update()
	
# do a bit of cleanup
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cv2.destroyAllWindows()
vs.stop()

# show the output image
cv2.imshow("Output", output)
cv2.waitKey(0)
