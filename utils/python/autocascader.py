from __future__ import print_function
import argparse
import ConfigParser
import os

from utils.youtube import download
from utils.video import markframes, extractimages
from utils.marker import updatemarkedframes, markobjects, viewobjects

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

# Frames - mark files directory
frames_mark_dir = os.path.join(script_dir, to_root,
                               config.get('paths', 'frames_mark_dir'))
frames_mark_glob = config.get('globs', 'frames_mark_file')

# Images directory
images_dir = os.path.join(script_dir, to_root,
                          config.get('paths', 'images_dir'))

# Objects
objects_mark_dir = os.path.join(script_dir, to_root,
                                config.get('paths', 'objects_mark_dir'))


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

parser.add_argument('--markframes', action='store_true',
                    help='mark frames to be: Front, Solaris front, Background or Nothing,\
                         press:\
                         Space - to pause display, \
                         F - to mark frame as any bus Front, \
                         S - to mark frame as Solaris bus front, \
                         B - to mark as Background, \
                         N - to Not mark at all (image won\'t be extracted)')

parser.add_argument('--updatemarkedframes', action='store_true',
                    help='if there wer to many images set to extract from video, i.e.: front instead\
                         of background or vice versa, etc. than one can remove extracted images. After\
                         that script with this flag must be run to update mark file - *.crlf representing\
                         marked frames to extract')

parser.add_argument('-e','--extractimages', action='store_true',
                    help='extracting images from downloaded videos according to "marked_frames_in_videos"\
                         description files')

parser.add_argument('--markobjects', action='store_true',
                    help='marking objects in images and store in opencv description file format')

parser.add_argument('--deleteobjects', action='store_true',
                    help='marking objects in images to be deleted from opencv description file by pressing d')

parser.add_argument('--viewobjects', action='store_true',
                    help='viewing objects in images by displaying rectangles around them')


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
if(args.markframes):
    print("\n==> MARKING FRAMES")
    markframes(yt_down_dir,frames_mark_dir)
if(args.updatemarkedframes):
    print("\n==> UPDATING FRAMES")
    updatemarkedframes(images_dir,frames_mark_dir)
if(args.extractimages):
    print("\n==> EXTRACTING FRAMES")
    extractimages(frames_mark_dir,yt_down_dir,images_dir)
if(args.markobjects):
    print("\n==> MARKING OBJECTS")
    markobjects(images_dir,objects_mark_dir)
if(args.viewobjects):
    print("\n==> VIEWING OBJECTS")
    viewobjects(images_dir,objects_mark_dir)
if(args.deleteobjects):
    print("\n==> DELETING OBJECTS")
    viewobjects(images_dir,objects_mark_dir, True)
    
    