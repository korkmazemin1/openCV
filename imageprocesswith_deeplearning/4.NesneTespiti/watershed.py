import cv2
import numpy as np
from imshow import plt_imshow,plt_imshow_gray
import matplotlib.pyplot as plt


image=cv2.imread("data\\watershed_coins.webp")
#lpfi blurring

coin_blur = cv2.medianBlur(image,7)
# gray formata çevrim
coin_gray =cv2.cvtColor(coin_blur,cv2.COLOR_BGR2GRAY)
#binary Threshold
ret,coin_thresh =cv2.threshold(coin_gray,75,255,cv2.THRESH_BINARY)
# kontur bulma
contours,hiearchy=cv2.findContours(coin_thresh.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    if hiearchy[0][i][3]==-1:
        cv2.drawContours(image,contours,i,(255,0,0),6)# konturları sırası ile çizdirme
cv2.imshow("i",image)
cv2.waitKey()        

#### Buraya kadar olan kısımlarda başarısız bir segmentasyon görülüyor

##WATERSHED##
image=cv2.imread("data\\watershed_coins.webp")
#lpfi blurring
coin_blur = cv2.medianBlur(image,7)
# gray formata çevrim
coin_gray =cv2.cvtColor(coin_blur,cv2.COLOR_BGR2GRAY)
#binary Threshold
ret,coin_thresh =cv2.threshold(coin_gray,65,255,cv2.THRESH_BINARY)
#açılma 
kernel= np.ones((3,3),np.uint8)
opening=cv2.morphologyEx(coin_thresh,cv2.MORPH_OPEN,kernel,iterations=3)

#nesneler arası mesafe distance
dist_transform=cv2.distanceTransform(opening,cv2.DIST_L2,5)# aradaki köprüler l2 yani öklid mesafeleri 
cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)# dist transform fonksiyonu normalize edilmeden çalışmıyor

cv2.imshow("dist_transform",dist_transform)
cv2.waitKey()
#nesneleri küçült 
ret,sure_foreground=cv2.threshold(dist_transform,0.4*np.max(dist_transform),255,0)
#max(dist_transform) ile maximum thresh değerini aldık
cv2.imshow("sure",sure_foreground)
cv2.waitKey()


#arka plan için resmi büyüt
sure_background = cv2.dilate(opening,kernel,iterations=2)
sure_foreground=np.uint8(sure_foreground)
# önplan ve arkaplan farkı alınır
unknown=cv2.subtract(sure_background,sure_foreground)
cv2.imshow("hey",unknown)
cv2.waitKey()
ret,marker =cv2.connectedComponents(sure_foreground)
marker=marker+1
marker[unknown == 255]= 0

marker = marker.astype(np.uint8)
cv2.imshow("test",marker)
cv2.waitKey()


markers=marker.copy()
marker=np.uint8(marker)

# Maksimum değeri belirle
max_value = np.max(marker)

# Arkaplan değerini belirlenen maksimum değerle aynı yap
marker[marker == 0] = max_value

cv2.imshow("marker",marker)

cv2.waitKey()
marker=np.uint8(marker)
cv2.imshow("before_water",marker)
cv2.waitKey()
marker=cv2.watershed(image,markers)
marker=np.uint8(marker)
cv2.imshow("after_water",marker)
cv2.waitKey()
contours,hiearchy=cv2.findContours(marker.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
for i in range(len(contours)):
    if hiearchy[0][i][3]==-1:
        cv2.drawContours(image,contours,i,(255,255,0),2)
cv2.imshow("ads",image)        
cv2.waitKey()