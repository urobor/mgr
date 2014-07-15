import glob
import os
import cv2
import numpy

PREFIX_DIR = "/home/kuba"

mser = cv2.MSER()

for image_file in glob.glob(os.path.join(PREFIX_DIR,"Magisterka/local/img/digits/all/*")):
    img = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    vis = img.copy()
    gray = cv2.blur(gray, (5,5))
    vis = cv2.blur(vis, (5,5))
    regions = mser.detect(gray, None)
    for region in regions:
        box = cv2.boundingRect(numpy.array([region], dtype=numpy.int32))
        width, height = box[2],box[3]
        if(10*width > height and
           10*height > width and
           height < img.shape[1]/4 and
           box[1]+height < img.shape[1]/2):
            cv2.rectangle(vis, (box[0],box[1]), (box[0]+width,box[1]+height), (0,255,0), 2)
        cv2.rectangle(vis, (box[0],box[1]), (box[0]+width,box[1]+height), (0,0,255))
    cv2.imshow('image',vis)
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)