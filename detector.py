import tensorflow
import numpy as np
import os
import cv2
from loadImages import imageProcessing

IMGSIZE = 100

image = cv2.imread('ASSETS/numbers.png')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
binary_image = cv2.bitwise_not(gray_image)
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

i = 0
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    specNum = binary_image[y:y+h, x:x+w]
    specNum = cv2.resize(specNum, (28, 28))
    specNum = 255 - specNum # White background with black digit

    cv2.imwrite(f"captured/num{i}.png", 255-imageProcessing(specNum)) 
    i+=1
    
# cv2.namedWindow('Contours', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('Contours', 900, 900)
# cv2.imshow('Contours', binary_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

