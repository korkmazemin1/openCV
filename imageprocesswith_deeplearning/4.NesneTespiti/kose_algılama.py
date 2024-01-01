import numpy as np 
import cv2
from imshow import plt_imshow,plt_imshow_gray

image_orig=cv2.imread("data\\sudoku(1).png",0)

image=np.float32(image_orig)

dst=cv2.cornerHarris(image,blockSize=2,ksize=3,k=0.04)# cornerharris ile köşe tespiti 
#blocksize =hangi komşuya bakacağımızı gösterir-ksize kerneli alır k ise bir freeparameter
plt_imshow_gray(dst)

dst=cv2.dilate(dst,None)
image[dst>0.2*dst.max()]=1# genişletme yöntemi kullanarak tespit edilen noktalar belirgin hale gelir
# köşeler 1 (siyah) oldu
plt_imshow_gray(image)
    
    ## shi toması algoritması ##

image=np.float32(image_orig)

corners=cv2.goodFeaturesToTrack(image,120,0.01,10)# özellik çıkarımında kullanılan bir fonksiyon
corners=np.int64(corners)

for i in corners:
    x,y=i.ravel()
    cv2.circle(image,(x,y),3,(200,200,200),cv2.FILLED)
plt_imshow_gray(image)    