import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras 
from keras import datasets, layers, models
import cv2
from loadImages import imageProcessing, processorLegacy
from detector import detector

IMGSIZE = 28
model = models.load_model('assets/models/alphabetModelV2.model')
output_labels = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

predArr = detector(cv2.imread('ASSETS/images/TESTING.png', cv2.IMREAD_GRAYSCALE))
# predArr = processorLegacy(cv2.imread('ASSETS/images/TESTING.png', cv2.IMREAD_GRAYSCALE))
# predArr = cv2.imread('assets/test/4.png', cv2.IMREAD_GRAYSCALE)
# predArr = cv2.resize(predArr, (IMGSIZE, IMGSIZE))
# predArr = 255 - predArr

# for img in predArr:
#   plt.imshow(img, cmap='gray')
#   plt.show()

xtest = np.array(predArr).reshape(-1,IMGSIZE,IMGSIZE,1)
xtest = xtest / 255

probs = model.predict(xtest)
preds = np.argmax(probs, axis=1)
print("\n\n\n")
for i in range(len(preds)):
  print(output_labels[preds[i]], end="")
print("\n\n\n")