import numpy as np 
import cv2
import matplotlib.pyplot as plt
from imshow import plt_imshow,plt_imshow_gray
from collections import deque

# nesne merkezini depolayacak veri tipi
buffer_size=16 # deque nun boyutu
pts =deque(maxlen =buffer_size)# deque tanımladık

##  mavi renk aralığı 
blue_lower = (84,98,0)
blue_upper = (179,255,255)

cap=cv2.VideoCapture(0)
# kameranın derinliği ve pikseli 
cap.set(3,960)
cap.set(4,480)

while True:
    success,img_orig=cap.read()

    if success:# eğer capture ederse if in içine girer
        blurred =cv2.GaussianBlur(img_orig,(11,11),0)#standart sapmayı 0 verdik 

        hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
        mask=cv2.inRange(hsv,blue_lower,blue_upper)# belirlenen mavi değrleri dışında maskelenş
        cv2.imshow("mask",mask)
        # morfolojik işlemler ile gürültüleri kaldırma
        mask=cv2.erode(mask,None,iterations=5)# beyaz bölgelerin sınırı küçülür
        mask=cv2.dilate(mask,None,iterations=5)# beyaz bölgelerin sınırı büyür
        # morphologyex de uygulanabilir
        cv2.imshow("mask2",mask)
    
        (contours,_)=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu
        center=None

        if len(contours)>0:
            #en büyük konturu al 
            c=max(contours,key=cv2.contourArea)# en büyük kontur alındı
            rect=cv2.minAreaRect(c)#en büyük konturu alan dörtgen belirlendi
            ((x,y),(width,height),rotation)  =rect  # dörtgenin verileri çekildi
            
            box=cv2.boxPoints(rect)
            box=np.int64(box)# özellikler kullanarak bir kutucuk yaptık

            #moment-- bir görüntünün yarıçap alan ağırlık merkezi vb özelliklerinin ağırlıkların ortalaması....
            M=cv2.moments(c)
            center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))# moments kullanarak merkez kordinatları alındı
            cv2.drawContours(img_orig,[box],0,(0,255,255),2)# kontur çizildi
            # takip algoritması
            pts.appendleft(center)
            for i in range (1,len(pts)):
                if pts[i-1] is None or pts[i] is None:continue
                cv2.line(img_orig,pts[i-1],pts[i],(0,255,0),3)# merkez konumunun son 16 elemanı çizilir ve nesnenin hareketi gösterilir
            cv2.circle(img_orig,center,5,(255,0,255),-1)# merkeze bir çember çizildi
        cv2.imshow("orig",img_orig)    


    if cv2.waitKey(1) & 0xFF ==ord('q'):break
            