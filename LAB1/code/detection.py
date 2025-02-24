import os
from unittest import result
import cv2
import utils
import numpy as np
import matplotlib.pyplot as plt


def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:A
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # Read the detectData.txt file
    """
    direct path to the folder detect read the text into lines run lines and 
    get the coordinate every time read pop the text put it in classify if 
    classify is face use green as rectangle if nonface use red continue until the lines empty 
    """
    detectpath = 'data/detect/'

    with open(dataPath, 'r') as file:
      lines = file.readlines()
      for line_index in range(len(lines)):
          if len(lines)==0:
            break  
          name, num = lines[0].split()
          num = int(num)
          img = cv2.imread(detectpath+name)
          gray_img = cv2.imread(detectpath + name, cv2.IMREAD_GRAYSCALE)
          lines.pop(0)
          for i in range(num):
            x0, y0, width, height = map(int, lines[0].split())
            x1 = x0 + width
            y1 = y0 + height
            if clf.classify(cv2.resize(gray_img[y0:y1, x0:x1], (19, 19))):
                color = (0, 255, 0)  # Green color for correctly classified
                cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness=3)
            else:
                color = (0, 0, 255)  # Red color for misclassified
                cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness=3)
            lines.pop(0)
          cv2.imshow('image', img)
          cv2.waitKey(0)
          cv2.destroyAllWindows()
          

    # End your code (Part 4)
