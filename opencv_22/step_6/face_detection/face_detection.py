import numpy as np
import cv2
import matplotlib.pyplot as plt

erkek=cv2.imread("images/input/emin.png",0)# foto gray formatta okundu 

kadin=cv2.imread("images/input/kadin.jpeg",0)

toplu=cv2.imread("images/input/toplu_foto.jpg",0)
# fotolar okundu

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")# cascade çekildi

eye_cascade=cv2.CascadeClassifier("haarcascade_eye.xml")

def detect_face(img):
    face_img=img.copy()# fotonun kopyasını aldık

    face_recs=face_cascade.detectMultiScale(face_img)# cascade ile tespit yapıldı

    for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi

    return face_img

def detect_eye(img):
    face_img=img.copy()# fotonun kopyasını aldık

    face_recs=eye_cascade.detectMultiScale(face_img)# cascade ile tespit yapıldı

    for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi

    return face_img




result=detect_face(erkek)
plt.imshow(result,cmap="gray")
plt.waitforbuttonpress()


result=detect_face(kadin)
plt.imshow(result,cmap="gray")
plt.waitforbuttonpress()


result=detect_face(toplu)
plt.imshow(result,cmap="gray")
plt.waitforbuttonpress()

result=detect_eye(erkek)
plt.imshow(result,cmap="gray")
plt.waitforbuttonpress()

result=detect_eye(kadin)
plt.imshow(result,cmap="gray")
plt.waitforbuttonpress()

