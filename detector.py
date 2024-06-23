import tensorflow
import numpy as np
import os
import cv2
from loadImages import imageProcessing
import matplotlib.pyplot as plt

def detector(fullImage):
    fullImage = cv2.GaussianBlur(fullImage, (5, 5), 0)
    binary_image = cv2.bitwise_not(fullImage)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    # print(len(contours))

    imgArr = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        specNum = binary_image[y:y+h, x:x+w]
        imgArr.append(255-imageProcessing(255-specNum))
    return imgArr