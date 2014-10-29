from __future__ import print_function
import cv2
import ConfigParser
import glob
import os
import operator

yt_tag = 'phototrans'
object_type = 'front'
RATIO = 1

PREFIX_DIR = "/home/kuba"
OPENCV_DESCRIPTION_FILES = os.path.join(PREFIX_DIR,"Magisterka/github/data/description_files/digits_opencv")
cascade_dir = os.path.join(PREFIX_DIR, "Magisterka/dropbox/opencv/detector")

all_neg_dir = os.path.join(PREFIX_DIR, "Magisterka/local/img/objects/all/n")
classifier_file = os.path.join(cascade_dir, "dev_front_5000_pos_5000_neg.xml")
cascade = cv2.CascadeClassifier(classifier_file)
counter_pos = 0
counter_neg = 0
counter_neg_all = 0

rectsDetected = []

def get_key():
    global img
    drawing_image = img.copy()
    k = cv2.waitKey()
    if k & 0xFF == ord(' '):
        return
    elif k & 0xFF == ord('d'):
        if len(rectsDetected) > 0:
            rectsDetected.pop()
            for rec in rectsDetected:
                x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
                cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
            cv2.imshow('image', drawing_image)
    get_key()

def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,img, width, height
    drawing_image = img.copy()

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            width = x - ix;
            height = y - iy;
            if(height/width != RATIO):
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
        rectsDetected.append(rectangle)
        
        for rec in rectsDetected:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(drawing_image,(x1,y1),(x2,y2),(100,225,175),2)
        cv2.imshow('image', drawing_image)

def getBusCoordinates(img, h):
    height, width, depth = img.shape
    small = cv2.resize(img, (width * h / height,h))
    rectsDetected = cascade.detectMultiScale(small, scaleFactor=1.1, minNeighbors=1, minSize=(50,50))
    if(len(rectsDetected) > 0):
        rectsDetected = (float(height)/float(h)*rectsDetected).astype(int)
    return list(rectsDetected)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_rectangle)

for bus_line_number in sorted(glob.glob(os.path.join(PREFIX_DIR, "Magisterka/local/img",yt_tag, '*'))):
    if(os.path.basename(bus_line_number) in ["0","01","05","07","1","2","3",
                                             "10", 
                                             "100","101","102","103","104","105","106","107","108","109",
                                             "11",
                                             "110","111","112","113","114","115","116","117","118","119",
                                             "12",
                                             "120","121","122","123","124","125","126","127","128","129",
                                             "13",
                                             "130","131","132","133","134","135","136","137","138","139",
                                             "14",
                                             "140","141","142","143","144","145","146","147","148","149",
                                             "15",
                                             "150","151","152","153","154","155","156","157","158","159",
                                             "16",
                                             "160","161","162","163","164","165","166","167","168","169",
                                             "17",
                                             "170","171","172","173","174","175","176","177","178","179",
                                             "18",
                                             "180","181","182","183","184","185","186","187","188","189",
                                             "19",
                                             "190","191","192","193","194","195","196","197","198","199",
                                             "20", 
                                             "200","201","202","203","204","205","206","207","208","209",
                                             "21",
                                             "210","211","212","213","214","215","216","217","218","219",
                                             "22",
                                             "220","221","222","223","224","225","226","227","228","229",
                                             "23",
                                             "230","231","232","233","234","235","236","237","238","239",
                                             "24",
                                             "240","241","242","243","244","245","246","247","248","249",
                                             "25",
                                             "250","251","252","253","254","255","256","257","258","259",
                                             "26",
                                             "260","261","262","263","264","265","266","267","268","269",
                                             "27",
                                             "270","271","272","273","274","275","276","277","278","279",
                                             "28",
                                             "280","281","282","283","284","285","286","287","288","289",
                                             "29",
                                             "290","291","292","293","294","295","296","297","298","299",
                                             "30", 
                                             "300","301","302","303","304","305","306","307","308","309",
                                             "31",
                                             "310","311","312","313","314","315","316","317","318","319",
                                             "32",
                                             "320","321","322","323","324","325","326","327","328","329",
                                             "33",
                                             "330","331","332","333","334","335","336","337","338","339",
                                             "34",
                                             "340","341","342","343","344","345","346","347","348","349",
                                             "35",
                                             "350","351","352","353","354","355","356","357","358","359",
                                             "36",
                                             "360","361","362","363","364","365","366","367","368","369",
                                             "37",
                                             "370","371","372","373","374","375","376","377","378","379",
                                             "38",
                                             "380","381","382","383","384","385","386","387","388","389",
                                             "39",
                                             "390","391","392","393","394","395","396","397","398","399",
                                             ]):
        continue
    img_dir = os.path.join(PREFIX_DIR, "Magisterka/local/img",yt_tag, bus_line_number)
    prefix=yt_tag+'_' + os.path.basename(bus_line_number) + '_'
    #prefix="220714_road_to_work_"
    dest_img_dir = os.path.join(PREFIX_DIR, "Magisterka/local/img/objects", object_type)
    pos_dir = os.path.join(dest_img_dir, 'p')
    neg_dir = os.path.join(dest_img_dir, 'n')
    print(pos_dir)

    for path in sorted(glob.glob(os.path.join(img_dir, "*"))):
        img = cv2.imread(os.path.join(OPENCV_DESCRIPTION_FILES, path))
        if(img is None):
            continue
        imgDisp = img.copy()
            
        rectsDetected = getBusCoordinates(img, 1000)
        cv2.putText(imgDisp,str(len(rectsDetected)), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 3)
        for rec in rectsDetected:
            x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
            cv2.rectangle(imgDisp, (x1,y1), (x2,y2), (0,0,255), thickness=2)
        cv2.imshow('image',imgDisp)
        
        k = cv2.waitKey(0)
        if k & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit(0)     
        if k & 0xFF == ord('n'):
            cv2.imwrite(os.path.join(all_neg_dir,prefix+"{0:03d}".format(counter_neg_all)+".png"), img)
            counter_neg_all+=1     
        if k & 0xFF == ord('t'):
            cv2.imwrite(os.path.join(neg_dir,prefix+"{0:03d}".format(counter_neg)+".png"), img)
            counter_neg+=1
        if k & 0xFF == ord('m'):
            get_key()
            for rec in rectsDetected:
                if(rec[2] > 10 and rec[3] > 10):
                    x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
                    obj = img[y1:y2,x1:x2]
                    cv2.imwrite(os.path.join(pos_dir,prefix+"{0:03d}".format(counter_pos)+".png"), obj)
                    counter_pos+=1
        if k & 0xFF == ord('c'):
            for rec in rectsDetected:
                if(rec[2] > 10 and rec[3] > 10):
                    x1,y1,x2,y2 = rec[0],rec[1],rec[0]+rec[2],rec[1]+rec[3]
                    obj = img[y1:y2,x1:x2]
                    cv2.rectangle(imgDisp, (x1,y1), (x2,y2), (0,255,0), thickness=2)
                    cv2.imshow('image',imgDisp)
                    cv2.imshow('object', cv2.resize(obj, (100,100)))
                    k = cv2.waitKey(0)
                    if k & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        exit(0)
                    if k & 0xFF == ord('p'):
                        print(os.path.join(pos_dir,prefix+"{0:03d}".format(counter_pos)+".png"))
                        cv2.imwrite(os.path.join(pos_dir,prefix+"{0:03d}".format(counter_pos)+".png"), obj)
                        counter_pos+=1
                    if k & 0xFF == ord('t'):
                        cv2.imwrite(os.path.join(neg_dir,prefix+"{0:03d}".format(counter_neg)+".png"), obj)
                        counter_neg+=1
                    if k & 0xFF == ord('n'):
                        cv2.imwrite(os.path.join(all_neg_dir,prefix+"{0:03d}".format(counter_neg_all)+".png"), obj)
                        counter_neg_all+=1
                    if k & 0xFF == ord('s'):
                        break