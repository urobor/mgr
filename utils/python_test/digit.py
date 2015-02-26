import cv2
import numpy as np
import glob
import os

SZ=20
bin_n = 128 # Number of bins

svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )

affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    return img

def hog(img):
    #ret2,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

#img = cv2.imread('digits.png')
#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

images = []
responses = []
for digit_dir in glob.glob('/home/kuba/Magisterka/dropbox/img/*'):
    try:
        digit = int(os.path.basename(digit_dir))
	for digit_image in glob.glob(os.path.join(digit_dir,'p/*')):
            images.append(cv2.cvtColor(cv2.resize(cv2.imread(digit_image),(20,30)),cv2.COLOR_BGR2GRAY))
            responses.append(digit)
        
    except ValueError:
        # if not digit dir, then:
        continue

#for image in images:
#        cv2.imshow('image', image)
#        cv2.waitKey(10)
#        print

# First half is trainData, remaining is testData
#train_cells = [ i[:50] for i in cells ]
#test_cells = [ i[50:] for i in cells]

######     Now training      ########################

#deskewed = map(deskew,images)
hogdata = map(hog,images)
trainData = np.float32(hogdata).reshape(-1,bin_n*4)
responses = np.float32(responses).reshape(-1,1)
print responses
svm = cv2.SVM()
svm.train(trainData,responses, params=svm_params)
svm.save('svm_data.dat')

######     Now testing      ########################

#deskewed = [map(deskew,row) for row in test_cells]
#hogdata = [map(hog,row) for row in deskewed]
#hogdata = [map(hog,row) for row in test_cells]
#testData = np.float32(hogdata).reshape(-1,bin_n*4)
result = svm.predict_all(trainData)

#for image in images:
    #cv2.imshow('image', image)
    #print(svm.predict(np.float32(hog(image))))
    #cv2.waitKey(0)

#######   Check Accuracy   ########################
mask = result==responses
correct = np.count_nonzero(mask)
print correct*100.0/result.size
