from __future__ import print_function
import glob
import os
import cv2
import numpy as np

from fileutils import count_lines

enum_formater = '{:02d}.{:s}-{:s}'
gathering_info_message = '\n-> Files Being updated:'
rel_path_prefix = '../../../../../local/img'

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

def updatemarkedframes(img_dir,description_files_directory):
    for i,vid_id in enumerate(os.listdir(img_dir)):
        vid_id_dir = os.path.join(img_dir, vid_id)
        image_type_in_frame = {}
        for image_type in os.listdir(vid_id_dir):
            if image_type.endswith('.vec') or image_type.endswith('.txt') or image_type == 'classifier':
                continue
            for image in os.listdir(os.path.join(vid_id_dir,image_type)):
                frame_number = os.path.splitext(image)[0]
                image_type_in_frame[int(frame_number)] = image_type
        print(enum_formater.format(i+1,vid_id), end="... ")
        mark_file_path = os.path.join(description_files_directory, vid_id + ".crlf")
        lines = count_lines(mark_file_path)
        f = open(mark_file_path, 'w')
        for i in range(lines):
            try:
                if image_type_in_frame[i+1] == 'front':
                    f.write('F\n')
                elif image_type_in_frame[i+1] == 'background':
                    f.write('B\n')
                elif image_type_in_frame[i+1] == 'solaris':
                    f.write('S\n')
                else:
                    f.write('\n')
            except KeyError:
                f.write('\n')
        f.close()
        print("DONE")
    
def markobjects(img_root_dir, objects_mark_dir):
    global image
    global ix,iy,drawing
    global rectangles_list
    
    for i,img_id_path in enumerate(glob.glob(os.path.join(img_root_dir, '*'))):
        for img_type_path in glob.glob(os.path.join(img_id_path, '*')):
            video_id = os.path.basename(img_id_path)
            object_mark_dir_with_id = os.path.join(objects_mark_dir,video_id)
            print(enum_formater.format(i+1,video_id,os.path.basename(img_type_path)), end="... ")
            if(not os.path.exists(object_mark_dir_with_id)):
                os.makedirs(object_mark_dir_with_id)
            marked_objects_file_path = os.path.join(object_mark_dir_with_id,os.path.basename(img_type_path) + ".txt")
            if(os.path.exists(marked_objects_file_path)):
                print("EXISTS SKIPPING")
                continue
            f = open(marked_objects_file_path, 'w')
            for image_path in glob.glob(os.path.join(img_type_path, '*')):
                rectangles_list = []
                rel_path = os.path.join(rel_path_prefix,video_id,os.path.basename(img_type_path),os.path.basename(image_path))
                if not img_type_path.endswith('background'):
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
                else:
                    marked_objects_row = rel_path
                f.write(marked_objects_row + '\n')
            f.close()
            print("DONE")
 
 
def viewobjects(img_root_dir, objects_mark_dir, delete_bounding_box=False):
    for i,img_id_path in enumerate(glob.glob(os.path.join(objects_mark_dir, '*'))):
        for img_type_path in glob.glob(os.path.join(img_id_path, '*')):
            if img_type_path.endswith('background.txt'):
                f = open(img_type_path, 'r')
                for line in f:
                    print(os.path.join(img_id_path,line))
                    image = cv2.imread(os.path.join(img_id_path,line).strip())         
                    cv2.imshow('image',image)
                    k = cv2.waitKey()
                    if delete_bounding_box:
                        if k & 0xFF == ord('d'):
                            
            #    f_updated = open(img_type_path+".fix", 'w')
                
                
                
            #print(img_type_path)
            #
            #f = open(img_type_path, 'r')
            #if delete_bounding_box:
            #    f_updated = open(img_type_path+".fix", 'w')
            #
            #for line in f:
            #    values = line.strip().split()
            #    (img_path, number_of_rectangles), coordinates = values[0:2], values[2:]
            #    image = cv2.imread(os.path.join(img_id_path,img_path))   
            #    for i in range(int(number_of_rectangles)):
            #        x1 = int(coordinates[i*4])
            #        y1 = int(coordinates[i*4+1])
            #        x2 = int(coordinates[i*4]) + int(coordinates[i*4+2])
            #        y2 = int(coordinates[i*4+1]) + int(coordinates[i*4+3])
            #        cv2.rectangle(image,(x1,y1),(x2,y2),(127,127,255),1)       
            #    cv2.imshow('image',image)
            #    k = cv2.waitKey()
            #    if delete_bounding_box:
            #        if k & 0xFF == ord('d'):
            #            pass
            #        else:
            #            f_updated.write(line);
                f.close()