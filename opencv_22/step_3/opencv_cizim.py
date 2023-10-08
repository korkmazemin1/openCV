import numpy as np 
import cv2
import matplotlib.pyplot as plt

black=np.zeros(shape=(512,512,3),dtype=np.int16)# siyah piksellerden oluşan 512-512 3 kanallı bir fotoğraf oluşturduk




plt.imshow(black)
plt.waitforbuttonpress()

cv2.rectangle(black,(10,10),(400,254),(255,0,0),2)# belirlediğimiz iki noktaya kalınlığı iki olan bir dörtgen çizdik

plt.imshow(black)# bgr da blue kanalına 255 versekde plt bunu RGB olarak okuduğu için kırmızı gözükür
plt.waitforbuttonpress()

cv2.circle(black,(80,80),70,(0,255,0),5)# sırasıyla konum yarıçap ver rengi verilen çember çizildi
cv2.circle(black,(400,400),50,(0,255,0),-5)# kalınlık değerinde eksik değer verirsek çemberin içi belirlenen renk ile dolar
cv2.line(black,(70,42),(45,300),(0,0,255),6)# yine konumlarını rengini ve kalınlığını verdiğimiz çizgiyi çizdik


plt.imshow(black)
plt.waitforbuttonpress()

