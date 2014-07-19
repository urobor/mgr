import glob
import os
import cv2
import numpy as np

TO_ROOT_DIR_SCRIPT = '../../..'
TO_ROOT_DIR_DESCRIPTION_FILE = '../../..'
IMG_ROOT_DIR = 'local/img'
MARKED_FILE_PATH = 'github/data/description_files/digits_opencv/8.txt'
RATIO = 1.5

bus_types = ('solaris', 'front')

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

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,image, width, height
    drawing_image = image.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            width = x - ix;
            height = y - iy;
            if(height/width != RATIO):
                diff = height/width - RATIO
                if(diff > 0):
                    width = height / RATIO
                if(diff < 0):
                    height = width * RATIO
            cv2.rectangle(drawing_image,(ix,iy),(ix + int(width), iy + int(height)),(0,225,225),2)
            cv2.imshow('image', drawing_image)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # file format:
        # img/img1.jpg  1  140 100 45 45 // relative_path number_of_rectangles x y width height
        # img/img2.jpg  2  100 200 50 50   50 30 25 25
        rectangle = (x, y, w, h) = ix, iy, int(width), int(height)
        rectangles_list.append(rectangle)
        
        for rec in rectangles_list:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
        cv2.imshow('image', drawing_image)
        
marked_files = {}
if(os.path.isfile(os.path.join(TO_ROOT_DIR_SCRIPT,MARKED_FILE_PATH))):
    f = open(os.path.join(TO_ROOT_DIR_SCRIPT,MARKED_FILE_PATH), 'r')
    for line in f:
        marked_files[line.split()[0]] = True
    f.close()

for image_set_dir in glob.glob(os.path.join(TO_ROOT_DIR_SCRIPT, IMG_ROOT_DIR, '*')):
    for bus_type in bus_types:
        for bus_front_image_type in glob.glob(os.path.join(image_set_dir, bus_type)):
            for image_path in glob.glob(os.path.join(bus_front_image_type, '*')):
                if marked_files.get(image_path):
                    continue
                f = open(os.path.join(TO_ROOT_DIR_SCRIPT,MARKED_FILE_PATH), 'a')
                rectangles_list = []
                cv2.namedWindow('image')
                cv2.setMouseCallback('image',draw_rectangle)
                image = cv2.imread(image_path)
                cv2.imshow('image',image)
                get_key()
                if(len(rectangles_list) > 0):
                    marked_objects_row = os.path.join(image_path) + " " + str(len(rectangles_list))
                    for rect in rectangles_list:
                        marked_objects_row += "  "
                        for val in rect:
                            marked_objects_row += str(val) + " "
                    print marked_objects_row
                    f.write(marked_objects_row + "\n")
                f.close()
                
                
                