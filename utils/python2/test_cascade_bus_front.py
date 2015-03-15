import glob
import cv2
import numpy as np
from os import rename,path

cv2.namedWindow('image')

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_front_5000_pos_5000_neg.xml'
cascade = cv2.CascadeClassifier(classifier_file)

all_occurences = 0
correct_hits = 0
wrong_hits = 0

PRECISSION = 5.0

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/front/front_detector/*')):

    old_file_name = path.splitext(path.basename(image_path))[0]
    ground_truth = old_file_name.split('-')
    ground_truth.pop(0)
    if(not len(ground_truth) > 0):
        continue
    rectangles_list = []
    ground_truth_list = []
    for rect in ground_truth:
        ground_truth_list.append(map(int, rect.split('_')))
        all_occurences += 1

    print "File: " + old_file_name
    image = cv2.imread(image_path)
    rectsDetected = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))

    for rec in ground_truth_list:
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), thickness=4)
        match = False
        matched_idx = 0
        for idx, gt_rec in enumerate(rectsDetected):
            x1d,y1d,x2d,y2d = gt_rec[0],gt_rec[1],gt_rec[0]+gt_rec[2],gt_rec[1]+gt_rec[3]
            if abs(rec[0] - gt_rec[0]) < rec[2] / PRECISSION and \
            abs(rec[1] - gt_rec[1]) < rec[3] / PRECISSION and \
            abs(rec[2] - gt_rec[2]) < rec[2] / PRECISSION and \
            abs(rec[3] - gt_rec[3]) < rec[3] / PRECISSION:
                match = True
                correct_hits += 1
                cv2.rectangle(image, (x1d,y1d), (x2d,y2d), (0,255,0), thickness=2)
                matched_idx = idx
        if(match):
            rectsDetected = np.delete(rectsDetected, matched_idx, 0)
    for gt_rec in rectsDetected:
        wrong_hits += 1
        x1d,y1d,x2d,y2d = gt_rec[0],gt_rec[1],gt_rec[0]+gt_rec[2],gt_rec[1]+gt_rec[3]
        cv2.rectangle(image, (x1d,y1d), (x2d,y2d), (0,0,255), thickness=2)

    #cv2.imshow('image', image)
    #k = cv2.waitKey()

    #if k & 0xFF == ord('q'):
    #    break

    print "Correct: " + str(correct_hits) + "/" + str(all_occurences) + \
          " FAILS: " + str(wrong_hits)
