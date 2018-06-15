from keras.preprocessing.image import img_to_array
from keras.models import load_model
import cv2
import numpy as np
model = load_model('signs6.model')

def predict(imin):
    image = imin.copy()
    # image = imin[0:80, 340:420]
    image = cv2.resize(image, (38, 38))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return model.predict(image)[0]