import glob
import cv2
import numpy as np
import sys
import os
import ConfigParser

cascade = cv2.CascadeClassifier('/home/kuba/Magisterka/github/data/description_files/classifiers/dev_13_lbp_all_posratio_999_maxfalse_01.xml')

SCALE_FACTOR = 1.1
MIN_NEIGHBORS = 1
MIN_SIZE = (24,24)
NEW_HEIGHT = 144.0

for image_path in sorted(glob.glob('*.png')):
    image = cv2.imread(image_path)
    width,height = image.shape[1],image.shape[0] #new size (w,h)
    dividor = height/NEW_HEIGHT
    new_width = int(width/dividor)
    print(new_width)
    image_resized = cv2.resize(image,(new_width,int(NEW_HEIGHT)))
    rects = cascade.detectMultiScale(image_resized,
                                     scaleFactor=SCALE_FACTOR,
                                     minNeighbors=MIN_NEIGHBORS,
                                     minSize=MIN_SIZE)
    rects = [ x * dividor for x in rects ]
    for x1, y1, width, height in rects:
        cv2.rectangle(image, (int(x1), int(y1)), (int(x1+width), int(y1+height)), (0, 0, 255), 2)
    cv2.imshow("number", image)
    #cv2.imshow("number_crop", image[int(y1):int(y1+int(height/3)),x1:x1+int(width/2)])
    cv2.waitKey()
    