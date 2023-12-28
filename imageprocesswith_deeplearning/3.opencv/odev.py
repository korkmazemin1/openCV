import numpy as np 
import cv2
from imshow import plt_imshow,plt_imshow_gray
import matplotlib.pyplot as plt

image=cv2.imread("data//golden_gate(1).jpg")# resim çekildi
#image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)# Resmin uzayı bgr dan rgb ye çekildi
print(image.shape)# resmin boyutları çekildi
print(image.shape[0])
print(0.8*image.shape[0])
x=int(0.8*image.shape[0])
y=int(0.8*image.shape[0])
print((x,y))


"""
image_resize=cv2.resize(image,(x,y))# resim 4/5 oranında yeniden boyutlandırıldı
plt_imshow(image)
plt_imshow(image_resize)

cv2.putText(image,"emin",(50,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),5)

plt_imshow(image)

_,thresh=cv2.threshold(image,50,255,cv2.THRESH_BINARY)
plt_imshow(thresh)

blur=cv2.GaussianBlur(image,(7,7),15)
plt_imshow(blur)
"""
laplacian=cv2.Laplacian(image,3,(5,5))#Laplacian gradyan uygulandığında, görüntüdeki belirgin kenarlar ve köşeler vurgulanır. 
#Bu, bir pikselin çevresindeki yoğunluk değişimlerini belirleyerek kenarları ve detayları ortaya çıkaran bir filtreleme işlemidir.
plt_imshow(laplacian)

histogram=cv2.calcHist([image],channels=[0],mask=None,histSize=[256],ranges=[0,256])
plt.figure() 
plt.plot(histogram)
plt.waitforbuttonpress()