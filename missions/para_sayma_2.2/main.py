import cv2 
import numpy as np 
from matplotlib import pyplot as plt

lower_red = np.array([0,50,50]) 
upper_red = np.array([10,255,255])
coin=cv2.imread("data\\input\\toocoin.jpeg")
coin=cv2.resize(coin,(404,500))# kötü sonuç alınırsa orijinal görüntüden devam et

gray_coin=cv2.cvtColor(coin,cv2.COLOR_BGR2GRAY)

ret,thresh=cv2.threshold(gray_coin,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)




kernel=np.ones((3,3),np.uint8)# blur uygulamak için çekirdek tanımlandı-kernel tanınmlarken mevzu büyük veya küçük olması değil optimal bir değer olmasıdır
opening=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

sure_bg=cv2.dilate(opening,kernel,iterations=3)

dist_transform=cv2.distanceTransform(opening,cv2.DIST_L2,5)#morpoloji uygulANMIŞ görüntülerden parların merkezlerine bağlı küçük daireler çizer
ret,sure_fg=cv2.threshold(dist_transform,0.6*dist_transform.max(),255,0)
#deneme----------
print(f"max:{dist_transform.max()}")
sure_fg=np.uint8(sure_fg)
cnts = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

min_area = 10
white_dots = []
for c in cnts:# bu döngüde önplan görüntüsündeki beyaz alanlar sayılarak para adedi bulunuyor
   area = cv2.contourArea(c)
   if area > min_area:
      cv2.drawContours(sure_fg, [c], -1, (36, 255, 12), 2)
      white_dots.append(c)

print("saptanan para adedi:",len(white_dots))

#deneme--------

unknown=cv2.subtract(sure_bg,sure_fg)

ret, markers = cv2.connectedComponents(sure_fg)

markers = markers+1


markers[unknown==255] = 0  

markers = cv2.watershed(coin,markers)
coin[markers == -1] = [255,0,0]
#sure_fg görüntüsü üzerinden gitmek daha mantıklı parça parça paraların merkezini veriyor çünkü 

""""
sure_fg=cv2.cvtColor(sure_fg,cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(sure_fg,cv2.HOUGH_GRADIENT,1,20,
 param1=50,param2=20,minRadius=0,maxRadius=80)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
 # draw the outer circle
 cv2.circle(sure_fg,(i[0],i[1]),i[2],(255,0,0),2)
 # draw the center of the circle
 cv2.circle(sure_fg,(i[0],i[1]),2,(255,0,0),3)

"""
#hsv ile çizilen dairelerin sayısı saptanmaya çalışıldı fakat düzensiz çizimler olduklarından başka bir yol aranıyor

"""
mask=cv2.inRange(coin,lower_red,upper_red)

circles = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,20,
 param1=200,param2=30,minRadius=0,maxRadius=80)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
 # draw the outer circle
 cv2.circle(mask,(i[0],i[1]),i[2],(255,0,0),2)
 # draw the center of the circle
 cv2.circle(mask,(i[0],i[1]),2,(255,0,0),3)

"""
cv2.imshow("back",sure_bg)
cv2.imshow("foreground",sure_fg)
#cv2.imshow("mask",mask)

cv2.imshow("final",coin)
cv2.waitKey(0)
cv2.destroyAllWindows()