import cv2
import glob
import numpy as np
from collections import defaultdict, OrderedDict
from os import rename,path
import math

front_detector = cv2.CascadeClassifier('ocv/cascade_front_5000_pos_5000_neg.xml')
number_detector = cv2.CascadeClassifier('ocv/cascade_number_450_pos_800_neg.xml')
digit_0_detector = cv2.CascadeClassifier('ocv/dev_0_330_pos_600_neg.xml')
digit_1_detector = cv2.CascadeClassifier('ocv/dev_1_600_pos_1500_neg.xml')
digit_2_detector = cv2.CascadeClassifier('ocv/dev_2_500_pos_900_neg.xml')
digit_3_detector = cv2.CascadeClassifier('ocv/dev_3_500_pos_1500_neg.xml')
digit_4_detector = cv2.CascadeClassifier('ocv/dev_4_500_pos_1500_neg.xml')
digit_5_detector = cv2.CascadeClassifier('ocv/dev_5_400_pos_800_neg.xml')
digit_6_detector = cv2.CascadeClassifier('ocv/dev_6_320_pos_500_neg.xml')
digit_7_detector = cv2.CascadeClassifier('ocv/dev_7_180_pos_360_neg.xml')
digit_8_detector = cv2.CascadeClassifier('ocv/dev_8_350_pos_700_neg.xml')
digit_9_detector = cv2.CascadeClassifier('ocv/dev_9_320_pos_600_neg.xml')
templates = defaultdict(list)

for digit_directory in glob.glob('img/template/?'):
    digit = int(path.basename(digit_directory))
    for img_path in glob.glob(path.join(digit_directory, '*')):
        templates[digit].append(cv2.imread(img_path, cv2.IMREAD_GRAYSCALE))

def read(digits, number, templates):
    read_str = ''
    score_2_digit_coord = OrderedDict()
    for digit_key in digits.keys():
        for d in digits[digit_key]:
            digit_img = number[d[1]:d[1]+d[3],d[0]:d[0]+d[2]]
            #print d
            digit_img = cv2.resize(digit_img, (120, 180))

            for t in templates[digit_key]:
                res = cv2.matchTemplate(digit_img,t,cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                digit_result = max_val*10000;
                #print "DK: " + str(digit_key) + " RES: " + str(digit_result)
                coord_2_digit = [digit_key, d[0]]
                score_2_digit_coord[digit_result] = coord_2_digit

            #cv2.imshow('test', digit_img)
            #k = cv2.waitKey()
    result_map = OrderedDict()
    maxi = 0
    for score in sorted(score_2_digit_coord.keys(),reverse=True):
        digit = score_2_digit_coord[score][0]
        x = score_2_digit_coord[score][1]
        #print "INI x: " + str(x) + "d: " + str(digit)

        if len(result_map.keys()) > 3:
            #print ">3 x: " + str(x) + "d: " + str(digit)
            break
        if not maxi:
            maxi = score
        if score < 0.50 * maxi:
            #print "toosmall x: " + str(x) + "d: " + str(digit)
            break
        too_close = False
        for stored_x in result_map.keys():
            if math.fabs(x - stored_x) < 6:
                too_close = True;
                break
        if too_close:
            continue
        #print "x: " + str(x) + "d: " + str(digit)
        result_map[x] = digit
    
    for x in sorted(result_map.keys()):
        read_str += str(result_map[x])
    return read_str 

def detect(detector, image, height, mini, maxi, neighbors, scale):
    (h,w) = image.shape
    width = float(w) * (float(height) / float(h))
    resized = cv2.resize(image, (int(width), height))
    rectsDetected = detector.detectMultiScale(resized,
            scaleFactor=scale, 
            minNeighbors=neighbors,
            minSize=(1,mini), #height 
            maxSize=(9999,maxi),
            )
    height, width = image.shape
    resized_height, resized_width = resized.shape
    multiply = float(height) / float(resized_height)
    return map(lambda x: np.int16(x*multiply), rectsDetected) 
i = 0
fronts_detected = 0
numbers_detected = 0
numbers_read_correctly = 0
for img_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/all/*')):
    i+=1
    old_file_name = path.splitext(path.basename(img_path))[0]
    bus_number_gt = old_file_name.split('-')[1]
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    fronts = detect(front_detector, gray, 300, 50, 250, 1, 1.1)
    #print "----"
    #print "f " + str(len(fronts))
    # get biggest
    if(len(fronts) > 0):
        fronts_detected += 1
        f = max(fronts, key=lambda x:x[3])
        x,y,w,h = f[0],f[1],f[2],f[3]
        upperleftcorner = gray[y:y+(h/3), x:x+(w/2)]
        numbers = detect(number_detector, upperleftcorner,
                150, 30, 200, 5, 1.01)
        #print "n " + str(len(numbers))
        if(len(numbers) > 0):
            numbers_detected +=1
            n = max(numbers, key=lambda x:x[3])
            number = upperleftcorner[n[1]:n[1]+n[3],n[0]:n[0]+n[2]]
            digitslists = defaultdict(list)
            digitslists[0] = detect(digit_0_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[0]) > 0):
                #print "0 " + str(len(digitslists[0]))
            digitslists[1] = detect(digit_1_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[1]) > 0):
                #print "1 " + str(len(digitslists[1]))
            digitslists[2] = detect(digit_2_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[2]) > 0):
                #print "2 " + str(len(digitslists[2]))
            digitslists[3] = detect(digit_3_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[3]) > 0):
                #print "3 " + str(len(digitslists[3]))
            digitslists[4] = detect(digit_4_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[4]) > 0):
                #print "4 " + str(len(digitslists[4]))
            digitslists[5] = detect(digit_5_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[5]) > 0):
                #print "5 " + str(len(digitslists[5]))
            digitslists[6] = detect(digit_6_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[6]) > 0):
                #print "6 " + str(len(digitslists[6]))
            digitslists[7] = detect(digit_7_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[7]) > 0):
                #print "7 " + str(len(digitslists[7]))
            digitslists[8] = detect(digit_8_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[8]) > 0):
                #print "8 " + str(len(digitslists[8]))
            digitslists[9] = detect(digit_9_detector, number, 110, 40, 110, 40, 1.01)
            #if(len(digitslists[9]) > 0):
                #print "9 " + str(len(digitslists[9]))

            #print "NUMBER: " + read(digitslists, number, templates)
            if(bus_number_gt == read(digitslists, number, templates)):
                numbers_read_correctly += 1
                
            print "f: " + str(fronts_detected) + \
                    " n: " + str(numbers_detected) + \
                    " r: " + str(numbers_read_correctly)



    # draw rectangle
    #for idf, front in enumerate(fronts):
    #    x1,y1,x2,y2 = front[0],front[1],front[0]+front[2],front[1]+front[3]
    #    cv2.rectangle(gray, (x1,y1), (x2,y2), (255), thickness=4)
        

    #cv2.imshow('image', number)
    #k = cv2.waitKey()

    #if k & 0xFF == ord('q'):
    #   break
