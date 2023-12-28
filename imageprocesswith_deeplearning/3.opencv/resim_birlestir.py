import cv2
import numpy as np

#yatay birleştirme

img1=cv2.imread("data\\paper.jpg")
img2=cv2.imread("data\\car.jpg")# resimler okundu
img1
img1=cv2.resize(img1,(300,300))
img2=cv2.resize(img2,(300,300))# birleştirme için yeniden boyutlandırıldı
horizontal=np.hstack((img1,img2))# aynı yığın içersinde yatay olarak olarak birleştirildi

cv2.imshow("horizental",horizontal)
cv2.waitKey(0)


# dikey birleştirme 

ver=np.vstack((img1,img2))# yığın içerisinde dikey olarak birleştirildi


cv2.imshow("ver",ver)
cv2.waitKey(0)
cv2.destroyAllWindows()