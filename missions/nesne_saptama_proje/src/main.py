
import cv2 
import numpy as np 
from datetime import datetime

lower_blue=np.array([100, 70,70])# hsv için mavi renginin sınırları belirlendi
upper_blue=np.array([130, 255, 255])


import cv2
cap=cv2.VideoCapture(0)
codec=fourcc = cv2.VideoWriter_fourcc(*'mp4v')# videyu kaydetmek için codec
frame_rate=30
resolution=(640,480)
now=datetime.now()# dosya katıt için datetime eklendi
namme=now.strftime("%A-%H-%M-%S")
record_name="C:\\openCV\\nesne_saptama_proje\\data\\output\\object_detection{}.mp4".format(namme)
record=cv2.VideoWriter(record_name,codec,frame_rate,resolution)
while True:    
    ret,frame=cap.read()# kareleri tak tak okumak için girdik burada girdiğimiz ret fonksiyondan çıkan true false değerini kare ise çıkan kare değerini karşılaması için yazıldı
    frame=cv2.flip(frame,1)# görüntü y ekseninde çevrildi 
    record.write(frame)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,lower_blue,upper_blue)# 4 adımlı bir mask işlemi uygulandı
    mask=cv2.erode(mask,(5,5),iterations=3)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,(5,5))
    mask=cv2.dilate(mask,(5,5),iterations=3)

    contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # mavi rengindeki cisimler ayırt edildikten sonra konturları bulundu
    center=None
    fw,fh=frame.shape[:2]
    for cnt in contours:
         x,y,w,h=cv2.boundingRect(cnt)# burada bulduğumuz konturların sol üst konumunun kordinatları x,y ve width height ile genişlik ve yükseklik ölçülerini aldık
         if h>=20:   
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)# rectangle fonksiyonu ile öncesinde bulmuş olduğumuz kordinatlar ile bir kare çizdik
         
         if h>=20:
            cv2.line(frame,(0,int(y+h/2)),(fh,int(y+h/2)),(0,0,0),2)# tespit edilen nesnenin merkezinden x ve y kordinatlarını belirten çizgiler eklendi
            cv2.line(frame,(int(x+w/2),0),(int(x+w/2),fw),(0,0,0),2)
         
               
            

      
    
    
    cv2.imshow("webcam",frame)
    cv2.imshow("webcam2",mask)
    
    if cv2.waitKey(30)& 0xFF==ord("q"):
        break
record.release()    
cap.release()  
cv2.destroyAllWindows() 


