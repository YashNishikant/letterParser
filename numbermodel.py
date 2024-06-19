import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras 
from keras import datasets, layers, models
import cv2
from loadImages import imageProcessingOperations

CATEGORIES = ['add','sub','mul','div','(',')','0','1','2','3','4','5','6','7','8','9']
model = models.load_model('models/mathoperationsV14.model')
IMGSIZE = 100

img = cv2.imread('ASSETS/plusTESTING.png', cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (IMGSIZE, IMGSIZE))
img = imageProcessingOperations(img)

predArr = [img]
xtest = np.array(predArr).reshape(-1,IMGSIZE,IMGSIZE,1)
xtest = 255 - xtest
xtest = xtest / 255

plt.imshow(xtest[0], cmap='gray')
plt.show()

probs = model.predict(xtest)
preds = np.argmax(probs, axis=1)
for i in range(len(preds)):
  print(CATEGORIES[preds[i]])