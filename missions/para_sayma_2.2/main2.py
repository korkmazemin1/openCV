from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy import ndimage
import argparse
import imutils
import cv2
import numpy as np
# terminalden kodu çalıştırmak için: watershedd.py --image  data/input/toocoin.jpeg(burada başka bir yolda kullanılabilir)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

image=cv2.imread(args["image"])

shifted=cv2.pyrMeanShiftFiltering(image,21,51)
cv2.imshow("Input", image)

gray_coin=cv2.cvtColor(shifted,cv2.COLOR_BGR2GRAY)

thresh=cv2.threshold(gray_coin,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

D=ndimage.distance_transform_edt(thresh)
localMax=peak_local_max(D,min_distance=20,labels=thresh)


markers=ndimage.label(localMax,structure=np.ones((3,3)))[0]

labels=watershed(-D,markers,mask=thresh)
print(len(np.unique(labels))-1)

for label in np.unique(labels):
    if label==0:
        continue

mask=np.zeros(gray_coin.shape,dtype="uint8")
mask[labels==label]=255 

cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if imutils.is_cv2() else cnts[1]
c=max(cnts,key=cv2.contourArea)

((x,y),r)=cv2.minEnclosingCircle(c)
cv2.circle(image,(int(x),int(y)),int(r),(0,255,0),2)
cv2.putText(image,"#{}".format(label),(int(x)-10,int(y)),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

cv2.imshow("output",image)
cv2.waitKey(0)
cv2.destroyAllWindows()