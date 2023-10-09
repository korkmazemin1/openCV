import numpy as np 
import cv2
import matplotlib

cap=cv2.VideoCapture(0)# sıfır parametresi ile webcame bağanırız
width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))#videonun enine erişiriz 
height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))# videonun yüksekliğine erişiriz

while True:
    ret,frame=cap.read()# framler--kareler-- tek tek okunur

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)# her bir frame gray formata çevrilir

    cv2.imshow("frame",gray)# gray formata çevrilen frameler gösterilir

    if cv2.waitKey(1) & 0xFF == ord("q"):# eğer q tuşuna basıldı ise
        break# videoyu durdur

cap.release   # kamera ile olan bağlantı kesilir
cv2.destroyAllWindows()# pencere kapanır
