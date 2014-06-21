from __future__ import print_function
import glob
import os
import cv2

from fileutils import count_lines

enum_formater = '{:02d}.{:s}'
gathering_info_message = '\n-> Fetching marked video ids'
downloading_message = '\n-> Downloading'

class State:
    solaris = 3
    frontbus = 1
    background = 2
    nothing = 0

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

def markframes(downloaded_videos_dir,marked_frames_directory):
    pause = False    
    state = 0
    for i, file_name in enumerate(os.listdir(downloaded_videos_dir)):
        print(enum_formater.format(i+1,file_name), end="... ")
        cap = cv2.VideoCapture(os.path.join(downloaded_videos_dir,file_name))
        mark_file_path = os.path.join(marked_frames_directory,os.path.splitext(file_name)[0] + ".crlf")
        if os.path.exists(mark_file_path):
            print("EXISTS")
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
        lines_in_file = count_lines(mark_file_path);
        # suddenly stopped working ;/
        if(frames_in_video != lines_in_file):
            print("ERROR")
            raise Exception("Wrong frames number, video: " + str(frames_in_video) + " != file:" + str(lines_in_file))
        
def extractimages(description_files_directory, downloaded_vid_dir, img_root_dir):
    for i,file_path in enumerate(glob.glob(os.path.join(description_files_directory, '*.crlf'))):
        vid_id = os.path.splitext(os.path.basename(file_path))[0]
        vid_path = os.path.join(downloaded_vid_dir,vid_id + ".mp4")
        print(enum_formater.format(i+1,vid_id), end="... ")
        if(os.path.exists(vid_path)):
            cap = cv2.VideoCapture(vid_path)
        else:
            raise Exception("File not found: " + vid_path)
        
        if not os.path.exists(img_root_dir):
            os.makedirs(img_root_dir)
        img_dir = os.path.join(img_root_dir, vid_id)
        if(os.path.exists(img_dir)):
            print("DIR EXISTS")
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
        mk_file.close()
        print("DONE")