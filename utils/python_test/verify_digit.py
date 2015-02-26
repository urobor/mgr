import glob
import cv2
import numpy as np
from os import rename,path

svm = cv2.SVM()
svm = cv2.RTrees()
bin_n = 4
svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=1)
var_types = np.array([cv2.CV_VAR_NUMERICAL] * 10 + [cv2.CV_VAR_CATEGORICAL], np.uint8)
#CvRTParams(10,10,0,false,15,0,true,4,100,0.01f,CV_TERMCRIT_ITER));
trees_params = dict(max_depth=10 )
f_set_path = '/home/kuba/Magisterka/dropbox/img/?'
f_subset_path = 'p/*'
s_set_path = '/home/kuba/Magisterka/local/img/test/digits/?'
s_subset_path = '*'

def hog(img):
    #ret2,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:15,:10], bins[15:,:10], bins[:15,10:], bins[15:,10:]
    mag_cells = mag[:15,:10], mag[15:,:10], mag[:15,10:], mag[15:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

#print "=> Training"

for bin_n in range(10, 200, 10):
    images = []
    responses = []
    for digit_dir in glob.glob(f_set_path):
        digit = int(path.basename(digit_dir))
        for digit_image in glob.glob(path.join(digit_dir,f_subset_path)):
            images.append(cv2.cvtColor(cv2.resize(cv2.imread(digit_image),(20,30)),cv2.COLOR_BGR2GRAY))
            responses.append(digit)
    for digit_path in glob.glob(s_set_path):
        digit = int(path.basename(digit_path))
        for image_path in glob.glob(path.join(digit_path,s_subset_path)):
            digit_image = cv2.imread(image_path)
            images.append(cv2.cvtColor(cv2.resize(digit_image,(20,30)),cv2.COLOR_BGR2GRAY))
            responses.append(digit)

    hogdata = map(hog,images)
    trainData = np.float32(hogdata).reshape(-1,bin_n*4)
    responses = np.float32(responses).reshape(-1,1)
    #svm.train(trainData,responses, params=svm_params)
    svm.train(trainData, cv2.CV_ROW_SAMPLE,responses)#, varType=var_types, params=trees_params)
    #result = svm.predict_all(trainData)
    #mask = result==responses
    #correct = np.count_nonzero(mask)

    #print "=> Verification"

    counter = 0
    all_ok = 0
    for digit_path in sorted(glob.glob(s_set_path)):
        true_digit = int(path.basename(digit_path))
        ok = 0
        digit_counter = 0
        for image_path in sorted(glob.glob(path.join(digit_path,s_subset_path))):
            digit_image = cv2.imread(image_path)
            prediction = int(svm.predict(np.float32(hog(cv2.resize(digit_image,(20,30))))))
            if true_digit == prediction:
                ok+=1
                all_ok+=1
            counter+=1
            digit_counter+=1
        #print ' {}   {:.2f}'.format(true_digit, float(ok)/float(digit_counter))
    #print ' {:3d} {:.2f} {:.2f}'.format(bin_n, correct*1.0/result.size, (float(all_ok)/float(counter)))
    print ' {:3d} {:.2f}'.format(bin_n,(float(all_ok)/float(counter)))

