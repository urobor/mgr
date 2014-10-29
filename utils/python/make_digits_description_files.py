from __future__ import print_function
import cv2
import ConfigParser
import glob
import os
import operator
from PIL import Image

PREFIX_DIR = "/home/kuba"
DIGITS_DIR = "Magisterka/local/img/objects"

for object_type_path in glob.glob(os.path.join(PREFIX_DIR,DIGITS_DIR,"*")):
    object_type = os.path.basename(object_type_path)
    if len(object_type) < 3:
        for sample_type_path in glob.glob(os.path.join(object_type_path, "*")):
            sample_type = os.path.basename(sample_type_path)
            name = object_type+"_"+sample_type+".txt"
            desc_file = open(os.path.join(PREFIX_DIR,DIGITS_DIR,name),'w')
            for sample_path in sorted(glob.glob(os.path.join(sample_type_path, "*"))):
                sample_name = os.path.basename(sample_path)
                line = os.path.join(object_type,sample_type,sample_name)
                if(sample_type == "p"):
                    line += " 1 0 0 60 90"
                desc_file.write(line+"\n")
            if("n" == sample_type):
                for all_neg_sample_path in sorted(glob.glob(os.path.join(PREFIX_DIR,DIGITS_DIR,"all","n","*"))):
                    desc_file.write(os.path.join('all','n',os.path.basename(all_neg_sample_path))+"\n")
            desc_file.close()
    if object_type == 'front':
        for sample_type_path in glob.glob(os.path.join(object_type_path, "*")):
            sample_type = os.path.basename(sample_type_path)
            name = object_type+"_"+sample_type+".txt"
            desc_file = open(os.path.join(PREFIX_DIR,DIGITS_DIR,name),'w')
            for sample_path in sorted(glob.glob(os.path.join(sample_type_path, "*"))):
                sample_name = os.path.basename(sample_path)
                im=Image.open(sample_path)
                line = os.path.join(object_type,sample_type,sample_name)
                if(sample_type == "p"):
                    line += " 1 0 0 " + str(im.size[0]) + " " + str(im.size[1])
                desc_file.write(line+"\n")
            if("n" == sample_type):
                for all_neg_sample_path in sorted(glob.glob(os.path.join(PREFIX_DIR,DIGITS_DIR,"all","n","*"))):
                    desc_file.write(os.path.join('all','n',os.path.basename(all_neg_sample_path))+"\n")
            desc_file.close()
        