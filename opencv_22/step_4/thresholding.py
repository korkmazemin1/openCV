import numpy as np
import cv2
import matplotlib.pyplot as plt

img=cv2.imread("opencv_22\\step_4\\rainbow.jpeg")# resim okundu
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#resim gray formata çevrildi

ret,thresh=cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)# 127 den büyük piksel değerlerini 255 e çeviri # ret threshold değerini alır

plt.imshow(thresh,cmap="gray")
plt.waitforbuttonpress()

ret,thresh1=cv2.threshold(thresh,127,255,cv2.THRESH_BINARY_INV)# siyah ve beyazlar yer değişir


def show_pic(img):# göstermeden önce yeniden boyutlandırdan fonksiyon
    fig=plt.figure(figsize=(15,15))# fotoğrafın ölçeği belirlendi
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")#colormapi belirledik
    plt.waitforbuttonpress()

show_pic(thresh)# fonksiyon thresh görseli için çağrıldı


image=cv2.imread("opencv_22\\step_4\\image.jpg",0)# fotoyu direkt gray olarak çektik

show_pic(image)

ret,th=cv2.threshold(image,127,255,cv2.THRESH_BINARY)# elle girilen threshold değeri bu resim için işe yaramaz

show_pic(th)

th2=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,8)# bu fonksiyon ile ortalama threshold hesaplanıp uygulanır#11 kaç tane piksel değerine bakılması gerektiğini belirtir duruma göre tek sayılar ile değiştirilebilir
# sabit bir parametre
show_pic(th2)

th3=cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C ,cv2.THRESH_BINARY,11,8)# bu fonksiyon ile ortalama threshold hesaplanıp uygulanır#11 kaç tane piksel değerine bakılması gerektiğini belirtir duruma göre tek sayılar ile değiştirilebilir
# sabit bir parametre
show_pic(th3)