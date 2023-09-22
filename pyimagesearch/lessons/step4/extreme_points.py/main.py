"""
Resimdeki elin yönlerini bulup noktalar ile gösteren miniprojenin algoritması

1-resim okundu
2-gray formata çevrildi
3-blur uygulandı
4-threshold uygulandı
5-gürültüleri kaldırmak için erode ve dilate fonksiyonları kullanıldı
6-konturlar saptandı ve dizi haline getirildi
7-konturların en büyüğü alınıp kuzey güney saptandı
8-sırasıyla konturlar çizildi ve yönleri belirten daireler resim üzerinde çizildi
9-sonuç resim gösterildi





"""

import cv2
import imutils
from datetime import datetime


image = cv2.imread("images/input/hand.png")# resim okundu
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#gray formata çevrildi
gray = cv2.GaussianBlur(gray, (5, 5), 0)# resime blur uygulandı

thresh=cv2.threshold(gray,45,255,cv2.THRESH_BINARY)[1]# threshold uyguland

thresh=cv2.erode(thresh,None,iterations=2)
thresh=cv2.dilate(thresh,None,iterations=2)
#erode ve dilate fonksiyonları thresholddan sonra küçük gürültüleri engellemek adına kullanıldı

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu
cnts=imutils.grab_contours(cnts)#konturları dizi haline getirir
c=max(cnts,key=cv2.contourArea)#alanı en yüksek olan konturu c ye atar

extLeft = tuple(c[c[:, :, 0].argmin()][0])# doğu yönünü gösteren en soldaki konturun kordinatı
extRight = tuple(c[c[:, :, 0].argmax()][0])# batı yönünü gösteren en sağdaki konturun kordinatı
extTop = tuple(c[c[:, :, 1].argmin()][0])# güney yönünü gösteren en soldaki konturun kordinatı
extBot = tuple(c[c[:, :, 1].argmax()][0])# kuzey yönünü gösteren en soldaki konturun kordinatı

cv2.drawContours(image,[c],-1,(0,255,255),2)
#konturu çizdik
cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
# yönlerin kontur üzerindeki en uç noktalarına daireler çizdik

now=datetime.now()
now=now.strftime('%Y_%m_%d_%H_%S')
cv2.imwrite(f"images/output/output_{now}.jpg",image)
cv2.imshow("image",image)
cv2.waitKey(0)