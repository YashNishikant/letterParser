import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

CHARSIZE = 50
IMGSIZE = 100

def centerSymbol(inputImg):
    binary_image = cv2.bitwise_not(inputImg)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.contourArea(c))
    x, y, w, h = cv2.boundingRect(contours[0])
    subImg = inputImg[y:y+h, x:x+w]
    subImg = cv2.erode(subImg, np.ones((3, 3), np.uint8), iterations=5)

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
        
    canvas = np.ones((IMGSIZE, IMGSIZE), dtype="uint8") * 255
    startX = (IMGSIZE - subImg.shape[1]) // 2
    startY = (IMGSIZE - subImg.shape[0]) // 2
    canvas[startY:startY+subImg.shape[0], startX:startX+subImg.shape[1]] = subImg
    _, thresh = cv2.threshold(canvas, 120, 255, cv2.THRESH_BINARY)
    return cv2.GaussianBlur(thresh, (5, 5), 0)


def plot_to_numpy_array():
    x = np.linspace(0, CHARSIZE)

    r = np.random.randint(0, 2) % 2
    if r == 0:
        y = 0.5 * np.random.randint(1, 6) * x
        print('lineq')
    else:
        a = np.random.randint(25, 30)
        b = np.random.randint(5, 10)
        y = (1/a) * pow((x + 10),2)
        print(a, b)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, CHARSIZE)
    ax.set_ylim(0, CHARSIZE)
    ax.plot(x, y, color='black')
    ax.axis('off')
    canvas = FigureCanvas(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    ncols, nrows = canvas.get_width_height()
    image = np.frombuffer(buf, dtype=np.uint8).reshape(nrows, ncols, 4)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    plt.close(fig)
    return image

def generateDivImg():
    return centerSymbol(plot_to_numpy_array())

for i in range(10):
    plt.imshow((generateDivImg()), cmap='gray')
    plt.show()
