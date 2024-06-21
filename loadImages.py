import os
import cv2
import numpy as np
import cv2
import matplotlib.pyplot as plt

IMGSIZE = 28
CHARSIZE = 20

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Add other image formats if needed
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path)
            img = imageProcessingOperations(img)
            plt.imshow(img, cmap='gray')
            plt.show()
            if img is not None:
                images.append(img)
    return images

def processorLegacy(inputImg): # ASSERT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT
    binary_image = cv2.bitwise_not(inputImg)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) == 0):
        return None
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[2]*cv2.boundingRect(c)[3]))
    x, y, w, h = cv2.boundingRect(contours[len(contours)-1])
    subImg = inputImg[y:y+h, x:x+w]

    subImg = resizeImageProportinal(subImg)

    plt.imshow(subImg, cmap='gray')
    plt.show()

    _, subImg = cv2.threshold(subImg, 250, 255, cv2.THRESH_BINARY)
    canvas = np.ones((IMGSIZE, IMGSIZE), dtype="uint8") * 255
    startX = int(IMGSIZE/2) - int(subImg.shape[1]/2)
    startY = int(IMGSIZE/2) - int(subImg.shape[0]/2)
    canvas[startY:startY+subImg.shape[0], startX:startX+subImg.shape[1]] = subImg
    return canvas

def imageProcessingOperations(inputImg): # ASSERT: IMAGE IS WHITE BACKGROUND WITH BLACK DIGIT

    subImg = resizeImageProportinal(inputImg)
    plt.imshow(subImg, cmap='gray')
    plt.show()
    canvas = np.ones((IMGSIZE, IMGSIZE), dtype="uint8") * 255
    startX = int(IMGSIZE/2) - int(subImg.shape[1]/2)
    startY = int(IMGSIZE/2) - int(subImg.shape[0]/2)
    canvas[startY:startY+subImg.shape[0], startX:startX+subImg.shape[1]] = subImg
    return canvas

def resizeImageProportinal(subImg):
    if(subImg.shape[1] > CHARSIZE and subImg.shape[1] > subImg.shape[0]):
        try:
            subImg = cv2.resize(subImg, (CHARSIZE, int(subImg.shape[0]/(subImg.shape[1]/CHARSIZE))))
        except Exception as e:
            subImg = cv2.resize(subImg, (CHARSIZE, 1))
    elif(subImg.shape[0] > CHARSIZE and subImg.shape[0] > subImg.shape[1]):
        try:
            subImg = cv2.resize(subImg, (int(subImg.shape[1]/(subImg.shape[0]/CHARSIZE)), CHARSIZE))
        except Exception as e:
            subImg = cv2.resize(subImg, (1, CHARSIZE))
    elif(subImg.shape[1] == subImg.shape[0]):
        subImg = cv2.resize(subImg, (CHARSIZE, CHARSIZE))

    return subImg