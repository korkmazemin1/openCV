import numpy as np
import cv2
import matplotlib.pyplot as plt


image=cv2.imread("opencv_22\\step_4\\image.jpg")
image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)# renk uzayı rgb ye döndü
image_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# renk uzayı graye döndü
def display(img):
    fig =plt.figure(figsize=(12,10))# resim yeniden boyutlandırılır
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")# gray formata çevrildi
    plt.waitforbuttonpress()

display(image_rgb)
display(image_gray)

image_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)# renk uzayı hsv yapıldı

plt.imshow(image_hsv)
plt.waitforbuttonpress()

kernel=np.ones((4,4),dtype=float)# 1 lerden oluşan bir kernel üretildi
kernel[kernel==1]=0.1# bütün sayılar 0.1 e çevrildi
print(kernel)
bil=cv2.bilateralFilter(image,9,75,75)

plt.imshow(bil)
plt.waitforbuttonpress()

sobelx=cv2.Sobel(image,cv2.CV_64F,1,0,ksize=5)# parametrelere bakarsan dx ve dy var eğer x sobel yapmak istiyorsan dx e 1 dy ye 0  ver
plt.imshow(sobelx)
plt.waitforbuttonpress()

color=("b","g","r")
for i,col in enumerate(color):# her renk kanalı için histogram tablosu oluşur
    histr=cv2.calcHist([image],[i],None,[256],[0,256])# her kanal için ayrı histogram açılır
    plt.plot(histr,color=col)
    plt.xlim([0,250])# aralığı belirledik
    plt.waitforbuttonpress()
plt.title("histogram")    




