import numpy as np
import cv2

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap=cv2.VideoCapture(0)
while 1:
    ret,frame=cap.read()
    face_frame=frame.copy()# fotonun kopyasını aldık

    face_recs=face_cascade.detectMultiScale(frame)# cascade ile tespit yapıldı

    for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi
    if cv2.waitKey(30) == 27:
      break
    cv2.imshow("face",frame)
cap.release()   
cv2.destroyAllWindows()


