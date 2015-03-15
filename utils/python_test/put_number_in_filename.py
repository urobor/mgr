import glob
import cv2
from os import rename,path

for image_path in sorted(glob.glob('/home/kuba/Magisterka/local/img/test/all/*')):
    image = cv2.imread(image_path)
    old_file_name = path.splitext(path.basename(image_path))[0]
    file_id = old_file_name.split('-')[1]
    cv2.imshow('image', image)
    print file_id
    k = cv2.waitKey()
    if k & 0xFF == ord('q'):
        break
