import numpy as np 
import cv2
import matplotlib.pyplot as plt


image=cv2.imread("opencv_22\\step_4\\sudoku.jpg")# resim okundu
image1=cv2.imread("opencv_22\\step_4\\rainbow.jpeg")#resim okundu
image2=cv2.imread("opencv_22\\step_4\\indir.png")

image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
image1=cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
image2=cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)# okunan resimlerin renk uzayları bgr dan rgb ye çevrildi

hist=cv2.calcHist([image1],channels=[0],histSize=[256],ranges=[0,256],mask=None)# histogram oluşturuldu

plt.plot(hist)
plt.waitforbuttonpress()

img=image

color=("b","g","r")# renk kanalları belirlendi

for i,col in enumerate(color):
    histr=cv2.calcHist([img],[i],None,[256],[0,256])# her kanal için ayrı histogram açılır
    plt.plot(histr,color=col)
    plt.xlim([0,250])# aralığı belirledik
    plt.waitforbuttonpress()
plt.title("histogram")    