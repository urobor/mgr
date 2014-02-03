from __future__ import print_function
import os
import subprocess
import re

script_directory = os.path.dirname(os.path.realpath(__file__))
description_files_directory = os.path.join(script_directory, '../data/description_files')
destination_directory = os.path.join(script_directory, '../../local/vid')

vid2itag = {}

print('=> Fetching marked video ids')

for csv_file in os.listdir(description_files_directory):
    if re.match('yt_marked.*\.csv', csv_file):
        print(' - ' + csv_file, end="... ")
        file_path = os.path.join(description_files_directory,csv_file)
        with open(file_path) as f:
            for line in f:
                vid, itag = line.strip().split(',')
                vid2itag[vid] = itag
            print(len(vid2itag))

print()
os.chdir(destination_directory)

print('=> Downloading')

prefix = ['youtube-dl', '--id', '-q', '-f']

i = 0
for id in vid2itag:
    i += 1
    print('{:02d}.{:s}'.format(i, id), end="... ")
    args = prefix + [vid2itag[id], id]
    if os.path.exists(os.path.join(destination_directory, id+'.mp4')):
        print("EXISTS")
    else:
        retcode = subprocess.call(args)
        if retcode:
            print("ERROR")
        else:
            print("DONE")