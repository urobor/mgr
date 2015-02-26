import glob
import cv2
import numpy as np
from os import rename,path

digits_dir = '/home/kuba/Magisterka/local/img/test/digits'

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/digits/0_detector/*')):
    old_file_name = path.splitext(path.basename(image_path))[0]
    if old_file_name.startswith('75Dz6s7sTg') \
    or old_file_name.startswith('aO71uxrP9B0') \
    or old_file_name.startswith('BJZLDmYMFvo') \
    or old_file_name.startswith('IHarVPkXwSg') \
    or old_file_name.startswith('jJ9ixBfVR5k') \
    or old_file_name.startswith('phototrans') \
    or old_file_name.startswith('jJ9ixBfVR5k'):
        continue

    ground_truth = old_file_name.split('-')
    ground_truth.pop(0)
    image = cv2.imread(image_path)

    ground_truth_list = []
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

    name = old_file_name.split('-')[0]
    number_string = old_file_name.split('_')[1]
    image = cv2.imread(image_path)
    
    coordinate_list = []
    for num,rec in enumerate(ground_truth_list):
        coordinate_list.append(rec[0])
    coord2digit = {}
    print old_file_name
    for num,x in enumerate(sorted(coordinate_list)):
        coord2digit[x] = number_string[num]

    for num,rec in enumerate(ground_truth_list):
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        digit_image = image[y1:y2,x1:x2]
        cv2.imshow(str(num),digit_image)
        #dir_path = path.join(digits_dir, coord2digit[x1])
        #cv2.imwrite(path.join(dir_path,name+'_'+str(num)+'.png'), digit_image)
    	k = cv2.waitKey(0)
        if k & 0xFF >= ord('0') and k & 0xFF <= ord('9'):
            dir_path = path.join(digits_dir, chr(k))
            cv2.imwrite(path.join(dir_path,name+'_'+str(num)+'.png'), digit_image)
    if k & 0xFF == ord('q'):
        break
