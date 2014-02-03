from __future__ import print_function
import glob
import os
import cv2

script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
raw_vid_dir = os.path.join(script_directory, '../../local/vid')
raw_img_dir = os.path.join(script_directory, '../../local/img')

for file_path in glob.glob(os.path.join(description_files_directory, '*.crlf')):
    print(file_path)
    vid_id = os.path.splitext(os.path.basename(file_path))[0]
    vid_path = os.path.join(raw_vid_dir,vid_id + ".mp4")
    if(os.path.exists(vid_path)):
        cap = cv2.VideoCapture(vid_path)
    else:
        raise Exception("File not found: " + vid_path)
    img_dir = os.path.join(raw_img_dir, vid_id)
    if(os.path.exists(img_dir)):
        print("DIRECTORY EXISTS SKIPPING: " + vid_id)
        continue
    else:
        os.mkdir(img_dir)
    
    mk_file = open(file_path, 'r')
    counter = 0
    for line in mk_file:
        counter += 1
        state, frame = cap.read()
        action = line.strip()
        if action == 'F':
            dest_path = os.path.join(img_dir, 'front')
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            cv2.imwrite(os.path.join(dest_path, "{0:0>6}.png".format(counter)), frame)
        elif action == 'B':
            dest_path = os.path.join(img_dir, 'background')
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            cv2.imwrite(os.path.join(dest_path, "{0:0>6}.png".format(counter)), frame)
        elif action == 'S':
            dest_path = os.path.join(img_dir, 'solaris')
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            cv2.imwrite(os.path.join(dest_path, "{0:0>6}.png".format(counter)), frame)
