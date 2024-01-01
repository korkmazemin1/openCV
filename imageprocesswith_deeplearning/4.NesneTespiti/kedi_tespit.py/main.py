import numpy as np
import cv2
import matplotlib.pyplot as plt

cat_cascade=cv2.CascadeClassifier("kedi.xml")
def detect_cat_face(img):
    face_img=img# fotonun kopyasını aldık

    face_recs=cat_cascade.detectMultiScale(face_img)# cascade ile tespit yapıldı

    for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi

    return face_img
cat=cv2.imread("kedi.jpg")
cat=detect_cat_face(cat)
cv2.imshow("cat",cat)
cv2.waitKey()