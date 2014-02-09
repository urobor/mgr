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

def get_key():
    global image
    drawing_image = image.copy()
    k = cv2.waitKey()
    if k & 0xFF == ord(' '):
        return
    elif k & 0xFF == ord('d'):
        if len(rectangles_list) > 0:
            rectangles_list.pop()
            for rec in rectangles_list:
                x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
                cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
            cv2.imshow('image', drawing_image)
    get_key()



def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,image
    drawing_image = image.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.rectangle(drawing_image,(ix,iy),(x,y),(0,225,225),2)
            cv2.imshow('image', drawing_image)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # file format:
        # img/img1.jpg  1  140 100 45 45 // relative_path number_of_rectangles x y width height
        # img/img2.jpg  2  100 200 50 50   50 30 25 25
        rectangle = (x, y, w, h) = ix, iy, x - ix, y - iy
        rectangles_list.append(rectangle)
        
        for rec in rectangles_list:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
        cv2.imshow('image', drawing_image)

for vid_id_path in glob.glob(os.path.join(raw_img_dir, '*')):
    for img_type_path in glob.glob(os.path.join(vid_id_path, '*')):
        if img_type_path.endswith('background') or img_type_path.endswith('.txt'):
            continue
        print(img_type_path)
        marked_objects_file_path = os.path.join(vid_id_path,img_type_path + ".txt")
        if(os.path.exists(marked_objects_file_path)):
            print("Mark file exists - SKIPPING")
            continue
        f = open(marked_objects_file_path, 'w')
        for image_path in glob.glob(os.path.join(img_type_path, '*')):
            rectangles_list = []
            rel_path = os.path.join(os.path.basename(img_type_path),os.path.basename(image_path))
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',draw_circle)
            image = cv2.imread(image_path)
            cv2.imshow('image',image)
            get_key()
            marked_objects_row = rel_path + " " + str(len(rectangles_list))
            for rect in rectangles_list:
                marked_objects_row += "  "
                for val in rect:
                    marked_objects_row += str(val) + " "
            f.write(marked_objects_row)
        f.close()
            