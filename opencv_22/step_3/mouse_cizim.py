import cv2
import numpy as np
import matplotlib.pyplot as plt

def daire_ciz(event,x,y,flags,param):# alıncak parametreler belirlendi
    
    if event== cv2.EVENT_LBUTTONDOWN :# eğer mouse üzerinden sol a tıklanırsa
        cv2.circle(img,(x,y),100,(0,255,0),thickness=-3)# yeşil içi dolu çember çiz--kordinatları setmousecallback fonksiyonundan alırız
    elif event ==cv2.EVENT_RBUTTONDOWN:#  eğer mouse üzerinden sağa a tıklanırsa
       cv2.circle(img,(x,y),100,(0,0,255),thickness=-3)# kırmızı içi dolu çember çiz

cv2.namedWindow(winname="deneme")

cv2.setMouseCallback("deneme",daire_ciz )













img=np.zeros((512,512,3))# siyah bir fotoğraf oluşturuldu

while True:
    cv2. imshow("deneme",img)

    if cv2.waitKey(20) & 0xFF ==27:# esc tuşuna basana kadar çerçeve açık kalır
        break

cv2.destroyAllWindows()    
