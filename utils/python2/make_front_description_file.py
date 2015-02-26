from __future__ import print_function
import cv2
import glob
import os
import operator

IMAGE_DIR = '/home/kuba/Magisterka/local/img/test/number/number_detector'
description_file_path = os.path.join(IMAGE_DIR, 'positive_description.txt')
desc_file = open(description_file_path,'w')

for image_path in glob.glob(os.path.join(IMAGE_DIR,"*")):
    file_name = os.path.basename(image_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    print(file_name_without_extension)
    if('positive_description' == file_name_without_extension):
        continue
    x,y,w,h = file_name_without_extension.split('-')[1].split('_')
    print(x + " " + y + " " + w + " " + h)
    line = file_name
    line += " 1 " + str(x) + " " + str(y) + " " + str(w) + " " + str(h)
    desc_file.write(line+"\n")
desc_file.close()
