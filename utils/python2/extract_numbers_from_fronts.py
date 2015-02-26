import glob
import cv2
import numpy as np
from os import rename,path

cv2.namedWindow('image')

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_number_2700_pos_3000_neg_n2_0997_04_pos.xml'
dest_dir = '/home/kuba/Magisterka/local/img/test/digits/0_detector'
cascade = cv2.CascadeClassifier(classifier_file)

all_occurences = 0
correct_hits = 0
wrong_hits = 0

PRECISSION = 3.0

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/number/number_detector/*')):

    old_file_name = path.splitext(path.basename(image_path))[0]
    ground_truth = old_file_name.split('-')
    ground_truth.pop(0)
    if(not len(ground_truth) > 0):
        continue
    rectangles_list = []
    ground_truth_list = []
    for rect in ground_truth:
        ground_truth_list.append(map(int, rect.split('_')))

    print "File: " + old_file_name
    image = cv2.imread(image_path)

    for rec in ground_truth_list:
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        #cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), thickness=4)
        if(y1 > 5):
            y1-=5
            y2+=5
        if(x1 > 5):
            x1-=5
            x2+=5
        cv2.imshow('number', image[y1:y2,x1:x2])
        cv2.imwrite(path.join(dest_dir,path.basename(image_path)),image[y1:y2,x1:x2])

    cv2.imshow('image', image)
    k = cv2.waitKey()

    if k & 0xFF == ord('q'):
        break

    print "Correct: " + str(correct_hits) + "/" + str(all_occurences) + \
          " FAILS: " + str(wrong_hits)
