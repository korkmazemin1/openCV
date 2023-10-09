import cv2
import numpy as np 
import time

cap=cv2.VideoCapture("opencv_22\\step_5\\inputs\\video.mp4")# video yüklendi

if cap.isOpened()==False:# eğer vide açılmadı ise uyarı ver
    print("videoya baglanilamadi")

while cap.isOpened():# video okunduysa
    ret,frame=cap.read()# framler tek tek okunur
    if ret==True:# video okundu ise
        cv2.imshow("frame",frame)# videoyu göster
        #time.sleep(1/25)# videonun hızını 1/25  oranında yavaşlattık

        if cv2.waitKey(20)  & 0xFF ==ord("q"):# q ya bastığında çık
            break
    

    else:
        break        # eğer video okunmadı ise videodan çık

cap.release()# video ile bağlantı kesildi
cv2.destroyAllWindows()    # pencereler kapatıldı