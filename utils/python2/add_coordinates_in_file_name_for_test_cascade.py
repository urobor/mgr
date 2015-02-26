import glob
import cv2
from os import rename,path

classifier_file = '/home/kuba/Magisterka/dropbox/opencv/detector/dev_front_5000_pos_5000_neg.xml'
cascade = cv2.CascadeClassifier(classifier_file)

ix,iy,drawing = -1,-1,False
rectangles_list = []
RATIO = 1

def get_key():
    global image
    drawing_image = image.copy()
    print rectangles_list
    for rec in rectangles_list:
        x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
    cv2.imshow('image', drawing_image)
    drawing_image = image.copy()
    k = cv2.waitKey()
    if k & 0xFF == ord('q'):
        return -1
    elif k & 0xFF == ord(' '):
        return 1
    elif k & 0xFF == ord('d'):
        if len(rectangles_list) > 0:
            rectangles_list.pop()
            for rec in rectangles_list:
                x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
                cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
            cv2.imshow('image', drawing_image)
    return get_key()

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,image, width, height
    drawing_image = image.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            width = x - ix;
            height = y - iy;
            if(width != 0 and height/width != RATIO):
                diff = height/width - RATIO
                if(diff > 0):
                    width = height / RATIO
                if(diff < 0):
                    height = width * RATIO
            cv2.rectangle(drawing_image,(ix,iy),(ix + int(width), iy + int(height)),(0,225,225),2)
            cv2.imshow('image', drawing_image)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # file format:
        # img/img1.jpg  1  140 100 45 45 // relative_path number_of_rectangles x y width height
        # img/img2.jpg  2  100 200 50 50   50 30 25 25
        rectangle = (x, y, w, h) = ix, iy, int(width), int(height)
        rectangles_list.append(rectangle)
        print rectangles_list

        for rec in rectangles_list:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
        cv2.imshow('image', drawing_image)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/front/front_detector/*')):

    old_file_name = path.splitext(path.basename(image_path))[0]
    if(len(old_file_name.split('-')) > 1):
        continue
    print "File: " + old_file_name
    image = cv2.imread(image_path)
    rectangles_list = []
    rectsDetected = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(1,1))

    for rec in rectsDetected:
        #x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
        #cv2.rectangle(image, (x1,y1), (x2,y2), (0,0,255), thickness=2)
        rectangles_list.append(rec)

    if(get_key() < 0):
        break
    new_file_name = ''
    for r in rectangles_list:
        part = '_'.join((str(r[0]),str(r[1]),str(r[2]),str(r[3])))
        if new_file_name != '':
          new_file_name = '-'.join((part, new_file_name))
        else:
          new_file_name = part
    new_file_name += ".jpg"
    new_file_name = '-'.join((old_file_name, new_file_name))
    rename(image_path, path.join(path.dirname(image_path), new_file_name))
