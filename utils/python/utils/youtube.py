from __future__ import print_function
import os
import subprocess
import re

enum_formater = '{:02d}.{:s}'
gathering_info_message = '\n-> Fetching marked video ids'
downloading_message = '\n-> Downloading'

def download(mark_files_dir, download_dir, yt_mark_mask='yt_marked.*\.csv'):
    vid2itag = {}
    print(gathering_info_message)
    for i, csv_file in enumerate(os.listdir(mark_files_dir)):
        if re.match(yt_mark_mask, csv_file):
            print(enum_formater.format(i+i,csv_file), end="... ")
            mark_file_path = os.path.join(mark_files_dir,csv_file)
            with open(mark_file_path) as f:
                for line in f:
                    vid, itag = line.strip().split(',')
                    vid2itag[vid] = itag
                print(len(vid2itag))
    print(downloading_message)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    os.chdir(download_dir)
    prefix = ['youtube-dl', '--id', '-q', '-f']
    for i, id in enumerate(vid2itag):
        print(enum_formater.format(i+1, id), end="... ")
        args = prefix + [vid2itag[id], id]
        if os.path.exists(os.path.join(download_dir, id+'.mp4')):
            print("EXISTS")
        else:
            retcode = subprocess.call(args)
            if retcode:
                print("ERROR")
            else:
                print("DONE")

