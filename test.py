import tensorflow
from tensorflow import keras
from keras import datasets, layers, models
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt

IMGSIZE = 100
CHARSIZE = 50
def imageProcessingOperations(inputImg): # ASSERT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT

    plt.imshow(inputImg, cmap='gray')
    plt.show()

    binary_image = cv2.bitwise_not(inputImg)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) == 0):
        return None
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[2]*cv2.boundingRect(c)[3]))
    x, y, w, h = cv2.boundingRect(contours[len(contours)-1])
    subImg = inputImg[y:y+h, x:x+w]

    print(subImg.shape)
    plt.imshow(subImg, cmap='gray')
    plt.show()

    if(subImg.shape[1] > CHARSIZE and subImg.shape[1] > subImg.shape[0]):
        print(1)
        try:
            subImg = cv2.resize(subImg, (CHARSIZE, int(subImg.shape[0]/(subImg.shape[1]/CHARSIZE))))
        except Exception as e:
            subImg = cv2.resize(subImg, (CHARSIZE, 1))
    elif(subImg.shape[0] > CHARSIZE and subImg.shape[0] > subImg.shape[1]):
        print(2)
        try:
            print("eee")
            print(f'{subImg.shape[1]}/({subImg.shape[0]}/{CHARSIZE}) = {int(subImg.shape[1]/(subImg.shape[0]/CHARSIZE))}')
            subImg = cv2.resize(subImg, (int(subImg.shape[1]/(subImg.shape[0]/CHARSIZE)), CHARSIZE))
        except Exception as e:
            print(e)
            subImg = cv2.resize(subImg, (1, CHARSIZE))

    print(subImg.shape)
    plt.imshow(subImg, cmap='gray')
    plt.show()

    _, subImg = cv2.threshold(subImg, 250, 255, cv2.THRESH_BINARY)
    subImg = cv2.erode(subImg, (5, 5), iterations=1)

    plt.imshow(subImg, cmap='gray')
    plt.show()

    canvas = np.ones((IMGSIZE, IMGSIZE), dtype="uint8") * 255
    startX = int(IMGSIZE/2) - int(subImg.shape[1]/2)
    startY = int(IMGSIZE/2) - int(subImg.shape[0]/2)
    canvas[startY:startY+subImg.shape[0], startX:startX+subImg.shape[1]] = subImg

    return cv2.GaussianBlur(canvas, (5, 5), 0) # OUTPUT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT
def imageProcessingOperationsDiv(inputImg): # ASSERT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT

    plt.imshow(inputImg, cmap='gray')
    plt.show()

    binary_image = cv2.bitwise_not(inputImg)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) == 0):
        return None
        
    contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)
    x1, y1, w1, h1 = cv2.boundingRect(contours[0])
    x2, y2, w2, h2 = cv2.boundingRect(contours[1])
    try:
        x3, y3, w3, h3 = cv2.boundingRect(contours[2])
    except Exception as e:
        x3, y3, w3, h3 = IMGSIZE+100, IMGSIZE+100, -IMGSIZE+100, -IMGSIZE+100

    # top left: min(x1,x2,x3), min(y1,y2,y3)
    # bottom right: max((x1+w1),(x2+w2),(x3+w3)), max((y1+h1),(y2+h2),(y3+h3))

    # top left:         x, y
    # bottom right:     x+w, y+h

    subImg = inputImg[min(y1,y2,y3):max((y1+h1),(y2+h2),(y3+h3)), min(x1,x2,x3):max((x1+w1),(x2+w2),(x3+w3))]
    subImg = cv2.resize(subImg, (CHARSIZE, CHARSIZE))
    _, subImg = cv2.threshold(subImg, 250, 255, cv2.THRESH_BINARY)
    plt.imshow(subImg, cmap='gray')
    plt.show()
    canvas = np.ones((IMGSIZE, IMGSIZE), dtype="uint8") * 255
    startX = int(IMGSIZE/2) - int(subImg.shape[1]/2)
    startY = int(IMGSIZE/2) - int(subImg.shape[0]/2)
    canvas[startY:startY+subImg.shape[0], startX:startX+subImg.shape[1]] = subImg
    return cv2.GaussianBlur(canvas, (5, 5), 0) # OUTPUT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT

img = cv2.imread('ASSETS/images/add/+_1018.jpg', cv2.IMREAD_GRAYSCALE)
#img = imageProcessingOperationsDiv(img)
img = imageProcessingOperations(img)
plt.imshow(img, cmap='gray')
plt.show()

# image = cv2.imread('ASSETS/numbers.png')
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# binary_image = cv2.bitwise_not(gray_image)
# contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    