from __future__ import print_function
import glob
import os
import cv2
import numpy as np


script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
raw_vid_dir = os.path.join(script_directory, '../../local/vid')
raw_img_dir = os.path.join(script_directory, '../../local/img')

image = np.zeros((512,512,3), np.uint8)
ix,iy,drawing = -1,-1,False

rectangles_list = []

for vid_id_path in glob.glob(os.path.join(raw_img_dir, '*')):
    for img_type_path in glob.glob(os.path.join(vid_id_path, '*')):
        if not img_type_path.endswith('.txt') or img_type_path.endswith('background.txt'):
            continue
        print(img_type_path)
        
        f = open(img_type_path, 'r')
        
        for line in f:
            values = line.strip().split()
            (img_path, number_of_rectangles), coordinates = values[0:2], values[2:]
            image = cv2.imread(os.path.join(vid_id_path,img_path))   
            for i in range(int(number_of_rectangles)):
                x1 = int(coordinates[i*4])
                y1 = int(coordinates[i*4+1])
                x2 = int(coordinates[i*4]) + int(coordinates[i*4+2])
                y2 = int(coordinates[i*4+1]) + int(coordinates[i*4+3])
                cv2.rectangle(image,(x1,y1),(x2,y2),(127,127,255),1)       
            cv2.imshow('image',image)
            cv2.waitKey()
        
        f.close()
            