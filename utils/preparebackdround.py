from __future__ import print_function
import glob
import os


script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
raw_vid_dir = os.path.join(script_directory, '../../local/vid')
raw_img_dir = os.path.join(script_directory, '../../local/img')


for vid_id_path in glob.glob(os.path.join(raw_img_dir, '*')):
    for img_type_path in glob.glob(os.path.join(vid_id_path, '*')):
        if not img_type_path.endswith('background') or img_type_path.endswith('.txt'):
            continue
        print(img_type_path)
        marked_objects_file_path = os.path.join(vid_id_path,img_type_path + ".txt")
        if(os.path.exists(marked_objects_file_path)):
            print("Mark file exists - SKIPPING")
            continue
        f = open(marked_objects_file_path, 'w')
        for image_path in glob.glob(os.path.join(img_type_path, '*')):
            rel_path = os.path.join(os.path.basename(img_type_path),os.path.basename(image_path))
            f.write(rel_path + "\n")
        f.close()
            