import glob
import os
import ConfigParser
import cv2

BACKGROUND_ROOT = "/home/kuba/Magisterka/github/data/description_files/opencv"
DIGITS_ROOT = "/home/kuba/Magisterka/github/data/description_files/digits_opencv"
DIGIT_BACKGROUND_FILE_NAME = "1_background.txt"

background = open(os.path.join(BACKGROUND_ROOT, "background.txt"))
digits_background = open(os.path.join(DIGITS_ROOT, DIGIT_BACKGROUND_FILE_NAME), "w")

for line in sorted(background):
    img = cv2.imread(os.path.join(BACKGROUND_ROOT, line.strip()))
    cv2.imshow('image',img)
    k = cv2.waitKey(0)
    if k & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        exit(0)
    if k & 0xFF == ord('d'):
        continue
    digits_background.write(line)
    
background.close()
digits_background.close()
    