from __future__ import print_function
import cv2
import ConfigParser
import glob
import os
import operator


def getBusCoordinates(img, h):
    height, width, depth = img.shape
    small = cv2.resize(img, (width * h / height,h))
    rectsDetected = cascade.detectMultiScale(small, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))
    if(len(rectsDetected) > 0):
        rectsDetected = (float(height)/float(h)*rectsDetected).astype(int)
    return rectsDetected

PREFIX_DIR = "/home/kuba"

OPENCV_DESCRIPTION_FILES = os.path.join(PREFIX_DIR,"Magisterka/github/data/description_files/digits_opencv")
    
cascade_dir = os.path.join(PREFIX_DIR, "Magisterka/github/data/description_files/classifiers")
test_dir = os.path.join(PREFIX_DIR, "Magisterka/github/data/tests")
script_dir = os.path.dirname(os.path.realpath(__file__))
script_name = os.path.splitext(os.path.basename(__file__))[0]

config = ConfigParser.ConfigParser()
config.read(os.path.join(script_dir, 'config', 'autocascader.ini'))
to_root = config.get('paths', 'script_to_root')

img_dir = os.path.join(script_dir, to_root,
                           config.get('paths', 'images_dir'))

def getRectsFromLine(line):
    splited = line.split()
    path = splited[0]
    numberOfRectangles = splited[1]
    rects = []
    for i in range(int(numberOfRectangles)):
        rect = []
        for j in range(2,6):
            rect.append(int(splited[(4*i)+j]))
        rects.append(rect)
    return path,rects

results = open(os.path.join(test_dir, "digit_8.txt"), "w")
results.write("pos matched, all pos, neg matched\n")

#for height in [600, 500, 400, 300, 200, 100]:
classifier_file = os.path.join(cascade_dir, "dev_digit8_lbp_default_513_pos_500_neg.xml")
cascade = cv2.CascadeClassifier(classifier_file)
#number = os.path.basename(classifier_file).split("_")[1]
#print(number)
positiveMatchedCounter = 0
allPositiveCounter = 0
negativeMatchedCounter = 0
path2rects = {}
positive = open(os.path.join(OPENCV_DESCRIPTION_FILES, "8.txt"))
#background = open(os.path.join(OPENCV_DESCRIPTION_FILES, "background.txt"))
for line in positive:
    path,rectsFromLine = getRectsFromLine(line)
    path2rects[path] = rectsFromLine
    allPositiveCounter += len(rectsFromLine)

for path in path2rects:
    img = cv2.imread(os.path.join(OPENCV_DESCRIPTION_FILES, path))
    rectsGroundTruth = path2rects[path] 
    rectsDetected = getBusCoordinates(img, 600)
        
    for rec in rectsDetected:
        found = False
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,0,255), thickness=6)
        for rec_gt in rectsGroundTruth:
            x1_gt,y1_gt,x2_gt,y2_gt = rec_gt[0],rec_gt[1],rec_gt[0]+rec_gt[2],rec_gt[1]+rec_gt[3]
            cv2.rectangle(img, (x1_gt,y1_gt), (x2_gt,y2_gt), (0,255,0), thickness=1)
            width_margin = rec[2]/4
            height_margin = rec[3]/4
            if(abs(x1 - x1_gt) < width_margin and
               abs(y1 - y1_gt) < height_margin and
               abs(x2 - x2_gt) < width_margin and
               abs(y2 - y2_gt) < height_margin):
                positiveMatchedCounter+=1
                found = True
        if(not found):
            negativeMatchedCounter+=1
            display
    cv2.imshow('image',img)
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)
    
results.write(str(positiveMatchedCounter) + "," +
              str(allPositiveCounter) + "," + str(negativeMatchedCounter) +"\n")
    
results.close()