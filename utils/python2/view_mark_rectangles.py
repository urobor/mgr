import glob
import cv2
from os import rename,path

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_digits_4700_pos_1000_neg.xml'

cv2.namedWindow('image')

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/digits/0_detector/*')):

    old_file_name = path.splitext(path.basename(image_path))[0]
    if(len(old_file_name.split('-')) > 1):
        print "File: " + old_file_name
        image = cv2.imread(image_path)
        (h,w,d) = image.shape
        print "h: " + str(h) + "; w: " + str(w)
        w_factor = float(w)/90.0 
        h_factor = float(h)/60.0
        drawing_image = image.copy()
        first = True
        new_name = [];
        for parts in old_file_name.split('-'):
            if(first):
                new_name.append(parts)
                first = False
                continue
            c = parts.split('_')
            x1 = float(float(c[0]) * w_factor)
            y1 = float(float(c[1]) * h_factor)
            width = float(float(c[2]) * w_factor)
            height = float(float(c[3]) * h_factor)
            print "ORGH: " + str(float(c[3])) + "; ORGW: " + str(float(c[2]))
            print "CALH: " + str(height) + "; CALW: " + str(width)
            print "## PROP = " + str(height/width)
            x2 = float((float(c[0])+float(c[2])) * w_factor)
            y2 = float((float(c[1])+float(c[3])) * h_factor)
            cv2.rectangle(drawing_image,
                    (int(x1),int(y1)),
                    (int(x2),int(y2)),
                    (100,255,175), 1)
            new_name.append("_".join([str(x1),str(y1),str(width),str(height)]))
        print "-".join(map(str,new_name)) + ".png";
    else:
        continue
    cv2.imshow('image',drawing_image) 
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        break
