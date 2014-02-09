from __future__ import print_function
import argparse
import ConfigParser
import os

from utils.youtube import download

script_dir = os.path.dirname(os.path.realpath(__file__))
script_name = os.path.splitext(os.path.basename(__file__))[0]

# Reading configuration
config = ConfigParser.ConfigParser()
config.read(os.path.join(script_dir, 'config', script_name + '.ini'))
to_root = config.get('paths', 'script_to_root')

# YouTube Directories
yt_mark_dir = os.path.join(script_dir, to_root,
                           config.get('paths', 'youtube_mark_dir'))
yt_down_dir = os.path.join(script_dir, to_root,
                           config.get('paths', 'youtube_download_dir'))
yt_mark_mask = config.get('masks', 'youtube_mark_file')


parser = argparse.ArgumentParser(description='Tool for:\
                                 1.Downloading marked videos from YouTube.\
                                 2.Marking desired frames: bus front present (solaris) or background.\
                                 3.Extracting marked frames and saving them as images.\
                                 4.Marking objects in images and preparing opencv description file.\
                                 5.Making opencv vector files from marked sets.\
                                 6.Training haar cascade detector and saving it in xml file.\
                                 7.Testing haar cascade detector against training data.')

parser.add_argument('-d','--download', action='store_true',
                    help='download all marked videos, marking files are in:\
                         "github/data/description_files/marked_for_download"')

#parser.add_argument('integers', metavar='N', type=int, nargs='*',
#                   help='an integer for tmport os')

#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

args = parser.parse_args()
#print(args.accumulate(args.integers))

if(args.download):
    print("\n==> DOWNLOADING")
    download(yt_mark_dir,yt_down_dir,yt_mark_mask)