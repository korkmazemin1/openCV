import cv2
import numpy as np 
import matplotlib.pyplot as plt

#kamera ayaları
cap=cv2.VideoCapture(0)#webcam açıldı

#bir adet frame oku

ret,frame=cap.read()

if ret==False:
    print("uyarı")

#detection
cv2