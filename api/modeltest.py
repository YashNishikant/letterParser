import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras 
from keras import datasets, layers, models
import cv2
from loadImages import imageProcessing, processorLegacy
from detector import detector
from openai import OpenAI
from apisecret import getSecret 
from PIL import Image
import numpy as np

client = OpenAI(
    api_key=getSecret()
)

def response(input):
  try:
    completion = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages = [
        {
          "role": "user",
          "content": input
        },
      ]
    )
    return completion.choices[0].message.content.strip()
  except:
    return "RATE LIMIT EXCEEDED"
  
def classify(arraydata):

  IMGSIZE = 28
  model = models.load_model('assets/models/alphabetModelV2.model')
  output_labels = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  img = Image.fromarray(arraydata)
  img.save('./assets/officialtesting/officialtest.png')
  img = cv2.imread('./assets/officialtesting/officialtest.png', cv2.IMREAD_GRAYSCALE)
  predArr = detector(img)
  finalstr = ""
  xtest = np.array(predArr).reshape(-1,IMGSIZE,IMGSIZE,1)
  xtest = xtest / 255
  probs = model.predict(xtest)
  preds = np.argmax(probs, axis=1)
  for i in range(len(preds)):
    finalstr+=output_labels[preds[i]]
  return [finalstr, ""]