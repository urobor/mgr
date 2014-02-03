from __future__ import print_function
import os
import cv2

script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
raw_vid_dir = os.path.join(script_directory, '../../local/vid')

pause = False    
state = 0

class State:
    solaris = 3
    frontbus = 1
    background = 2
    nothing = 0
    
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def get_key(delay, pause, state):
    k = cv2.waitKey(delay)
    if k & 0xFF == ord(' '):
        if pause:
            pause = False
        else:
            pause = True
    elif k & 0xFF == ord('f'):
        state = State.frontbus
    elif k & 0xFF == ord('b'):
        state = State.background
    elif k & 0xFF == ord('n'):
        state = State.nothing
    elif k & 0xFF == ord('s'):
        state = State.solaris
    return(state, pause)

for file_name in os.listdir(raw_vid_dir):
    print(file_name)
    cap = cv2.VideoCapture(os.path.join(raw_vid_dir,file_name))
    mark_file_path = os.path.join(description_files_directory,os.path.splitext(file_name)[0] + ".crlf")
    if os.path.exists(mark_file_path):
        print("EXISTS SKIPPING")
        continue
    frames_in_video = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
    f = open(mark_file_path, 'w')
    while(True):
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame',frame)
        if pause:
            state, pause = get_key(0, pause, state)
        state, pause = get_key(1, pause, state)
        if state == State.frontbus:
            print("FRONT")
            f.write('F\n')
        elif state == State.background:
            print("BACKGROUND")
            f.write('B\n')
        elif state == State.solaris:
            print("SOLARIS")
            f.write('S\n')
        else:
            f.write('\n')
    f.close()
    if(frames_in_video != file_len(mark_file_path)):
        print("ERROR")
        raise Exception("Wrong frames number, in text file and video file do not match")