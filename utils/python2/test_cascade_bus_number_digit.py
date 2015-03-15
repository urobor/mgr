import glob
import cv2
import numpy as np
from os import rename,path
from collections import defaultdict
import operator

cv2.namedWindow('image')

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_digits_4700_pos_1000_neg.xml'
cascade = cv2.CascadeClassifier(classifier_file)

all_occurences = 0
correct_hits = 0
wrong_hits = 0

PRECISSION = 3.0
X1_PRECISSION = 5.0
FRONT_HEIGHT = 70
MIN_SIZE = 40 #height 
MAX_SIZE = 60
SCALE_FACTOR = 136
min_neighbors = 1

def detect_scaled(image, cascade, front_height, min_width,
        max_size, scale_factor, min_neighbors):
    (h,w,d) = image.shape
    width = float(w) * (float(front_height) / float(h))
    #print "h " + str(h) + "; w " + str(w)
    resized = cv2.resize(image, (int(width), front_height))
    #cv2.imshow('resized', resized)
    #min_width = int(float(front_height)/min_width_div)
    #min_width = int(float(front_height)/10.0)
    rectsDetected = cascade.detectMultiScale(resized,
            scaleFactor=scale_factor, 
            minNeighbors=min_neighbors,
            minSize=(1,min_width), #height 
            maxSize=(75,max_size),
            )
    height, width, depth = image.shape
    resized_height, resized_width, depth = resized.shape
    multiply = float(height) / float(resized_height)
    return map(lambda x: np.int16(x*multiply), rectsDetected) 

def removeDoubles(rects):
    if(len(rects) > 0):
        print "---"
        rects_to_export = defaultdict(list)
        lengths = defaultdict(int)
        for rect in sorted(rects, key=lambda x:x[3]):
            rects_to_export[rect[3]].append(rect)
         
        for k,l in rects_to_export.iteritems():
            lengths[k] = len(l)

        maxKey = max(rects_to_export.iterkeys(), key=lambda key:len(rects_to_export[key]))
        return rects_to_export[maxKey]
    return rects
    #return sorted(rects, key=lambda x:x[3])[:3]
#for min_neighbors in range(1,10):
correct_hits = wrong_hits = all_occurences = 0

all_occurences = 0
correct_hits = 0
wrong_hits = 0
for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/digits/0_detector/*')):

    old_file_name = path.splitext(path.basename(image_path))[0]
    ground_truth = old_file_name.split('-')
    ground_truth.pop(0)
    if(not len(ground_truth) > 0):
        continue
    rectangles_list = []
    ground_truth_list = []
    #print "File: " + old_file_name
    image = cv2.imread(image_path)
    imageR = cv2.resize(image, (900, 600))
    source_image = image.copy()
    (h,w,d) = image.shape
    w_factor = float(w)/90.0 
    h_factor = float(h)/60.0
    for rect in ground_truth:
        c = rect.split('_')
        c[0] = int(float(c[0]) * w_factor)
        c[1] = int(float(c[1]) * h_factor)
        c[2] = int(float(c[2]) * h_factor)
        c[3] = int(float(c[3]) * h_factor)
        ground_truth_list.append(c)
        all_occurences += 1

    rectsDetected = detect_scaled(image, cascade, FRONT_HEIGHT, 
            MIN_SIZE,
            MAX_SIZE, float(SCALE_FACTOR)/100, min_neighbors)
    rectsDetected = removeDoubles(rectsDetected)
    for rec in ground_truth_list:
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        ws = (900.0/float(w))
        hs = (600.9/float(h))
        x1r = int(float(x1)*ws)
        x2r = int(float(x2)*ws)
        y1r = int(float(y1)*hs)
        y2r = int(float(y2)*hs)
        cv2.rectangle(imageR, (x1r,y1r), (x2r,y2r), (255,0,0), thickness=4)
        match = False
        matched_idx = 0
        counter_idx = 0
        for idx, gt_rec in enumerate(rectsDetected):
            x1d,y1d,x2d,y2d = gt_rec[0],gt_rec[1],gt_rec[0]+gt_rec[2],gt_rec[1]+gt_rec[3]
            #print str(idx)+"="+str(x1d)+";",
            #cv2.imshow(str(counter_idx), source_image[y1d:y2d,x1d:x2d])
            if abs(rec[0] - gt_rec[0]) < gt_rec[2] / X1_PRECISSION and \
            abs(rec[1] - gt_rec[1]) < gt_rec[2] / PRECISSION and \
            abs(rec[2] - gt_rec[2]) < gt_rec[2] / PRECISSION and \
            abs(rec[3] - gt_rec[3]) < gt_rec[2] / PRECISSION:
                match = True
                correct_hits += 1
                x1d = int(x1d * ws)
                x2d = int(x2d * ws)
                y1d = int(y1d * hs)
                y2d = int(y2d * hs)
                cv2.rectangle(imageR, (x1d,y1d), (x2d,y2d), (0,255,0), thickness=2)
                matched_idx = idx
            counter_idx+=1
        if(match):
            rectsDetected = np.delete(rectsDetected, matched_idx, 0)
    #print 
    for gt_rec in rectsDetected:
        wrong_hits += 1
        x1d,y1d,x2d,y2d = gt_rec[0],gt_rec[1],gt_rec[0]+gt_rec[2],gt_rec[1]+gt_rec[3]
        x1d = int(x1d * ws)
        x2d = int(x2d * ws)
        y1d = int(y1d * hs)
        y2d = int(y2d * hs)
        cv2.rectangle(imageR, (x1d,y1d), (x2d,y2d), (0,0,255), thickness=2)
    cv2.imshow('image', imageR)
    k = cv2.waitKey()

    if k & 0xFF == ord('q'):
        break
    #if k & 0xFF == ord('s'):
    #    cv2.imwrite(to_image_path, image)
    #path_to_write = '/home/kuba/Magisterka/local/img/test/digits/sample'  
    #to_image_path = path.join(path_to_write,path.basename(image_path))
print "4700_pos_1000_neg_0" + str(FRONT_HEIGHT) + "_h_" + \
      str(MIN_SIZE) + "_min_" + str(MAX_SIZE) + "_max_" + \
      str(SCALE_FACTOR) + "_sf_" + str(min_neighbors) + "_mn       " + \
      str(correct_hits) + "/" + str(all_occurences) + \
      ";" + str(wrong_hits)


