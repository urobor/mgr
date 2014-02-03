from __future__ import print_function
import glob
import os

script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
raw_vid_dir = os.path.join(script_directory, '../../local/vid')
raw_img_dir = os.path.join(script_directory, '../../local/img')

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

for vid_id in os.listdir(raw_img_dir):
    vid_id_dir = os.path.join(raw_img_dir, vid_id)
    image_type_in_frame = {}
    for image_type in os.listdir(vid_id_dir):
        for image in os.listdir(os.path.join(vid_id_dir,image_type)):
            frame_number = os.path.splitext(image)[0]
            image_type_in_frame[int(frame_number)] = image_type
    mark_file_path = os.path.join(description_files_directory, vid_id + ".crlf")
    lines = file_len(mark_file_path)
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