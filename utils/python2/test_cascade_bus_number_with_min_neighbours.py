import glob
import cv2
import numpy as np
from os import rename,path
import sys

cv2.namedWindow('image')

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_number_2800_pos_2800_neg_n2_09995_pos.xml'
cascade = cv2.CascadeClassifier(classifier_file)

all_occurences = 0
correct_hits = 0
wrong_hits = 0

PRECISSION = 3.0
FRONT_HEIGHT = 300

def detect_scaled(image, cascade, front_height,
        max_width, min_width, min_neighbors):
    resized = cv2.resize(image, (front_height, front_height))
    rectsDetected = cascade.detectMultiScale(resized,
        scaleFactor=1.1, minNeighbors=min_neighbors, 
        minSize=(min_width,min_width), 
        maxSize=(max_width,max_width))
    height, width, depth = image.shape
    resized_height, resized_width, depth = resized.shape
    multiply = float(height) / float(resized_height)
    return map(lambda x: np.int16(x*multiply), rectsDetected) 

for x in range(1, 10): 
    correct_hits = wrong_hits = all_occurences = 0
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
            all_occurences += 1

        sys.stdout.write("File: " + old_file_name + "\r")
        sys.stdout.flush()
        image = cv2.imread(image_path)
        rectsDetected = detect_scaled(image, cascade, FRONT_HEIGHT, 
            int(float(FRONT_HEIGHT)/float(4)), 
            int(float(FRONT_HEIGHT)/float(10)),
            x)

        for rec in ground_truth_list:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), thickness=4)
            match = False
            matched_idx = 0
            for idx, gt_rec in enumerate(rectsDetected):
                x1d,y1d,x2d,y2d = gt_rec[0],gt_rec[1],gt_rec[0]+gt_rec[2],gt_rec[1]+gt_rec[3]
                if abs(rec[0] - gt_rec[0]) < gt_rec[2] / PRECISSION and \
                abs(rec[1] - gt_rec[1]) < gt_rec[2] / PRECISSION and \
                abs(rec[2] - gt_rec[2]) < gt_rec[2] / PRECISSION and \
                abs(rec[3] - gt_rec[3]) < gt_rec[2] / PRECISSION:
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

    print str(x) + ";" + str(correct_hits) + "/" + str(all_occurences) + \
          ";" + str(wrong_hits)
