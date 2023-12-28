import cv2
import numpy as np 
import matplotlib.pyplot as plt

image=cv2.imread("data\\manzara1.jpg")# resim okundu
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# threshold(eşik) işlemi uygulamak için gray formatına çevirdik

plt.figure()
plt.imshow(image,cmap="gray")# siyah beyaz renk uzayında görüntüledik
plt.waitforbuttonpress()
plt.axis("off")# eksenlerin gözükmesini kapattık

#threshold eşikleme işlemi

_,thresh_img=cv2.threshold(image,40,255,cv2.THRESH_BINARY)# 60 üstündeki değerleri atacak bu binary için geçerli 
_,thresh_img2=cv2.threshold(image,40,255,cv2.THRESH_BINARY_INV)# burada ise tam tersi işlem yapıldı 60 altındaki değerler kapatıldı(beyaz yapıldı)
plt.figure()
plt.imshow(thresh_img,cmap="gray")# siyah beyaz renk uzayında görüntüledik
plt.waitforbuttonpress()
plt.figure()
plt.imshow(thresh_img2,cmap="gray")# siyah beyaz renk uzayında görüntüledik
plt.waitforbuttonpress()

# yukarıdaki eşikleme işleminde bütün bir görüntüde aynı eşik değeri uygulanır

#adaptive threshold -uyarlamalı

thresh_img2=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,21,8)# C sabitinde çıkarılabilecek değere 8 değerini veriyoruz ,11 ise piksel topluluklarının 11 piksel olduğunu belirtir

plt.figure()
plt.imshow(thresh_img2,cmap="gray")
plt.axis("off")
plt.waitforbuttonpress()