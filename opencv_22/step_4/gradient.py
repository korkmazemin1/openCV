import numpy as np 
import cv2 
import matplotlib.pyplot as plt

image=cv2.imread("opencv_22\\step_4\\sudoku.jpg")# resim okundu

def display(img):
    fig =plt.figure(figsize=(12,10))# resim yeniden boyutlandırılır
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")# gray formata çevrildi
    plt.waitforbuttonpress()

display(image)

sobelx=cv2.Sobel(image,cv2.CV_64F,1,0,ksize=3)# parametrelere bakarsan dx ve dy var eğer x sobel yapmak istiyorsan dx e 1 dy ye 0  ver
display(sobelx)

sobely=cv2.Sobel(image,cv2.CV_64F,0,1,ksize=3)# parametrelere bakarsan dx ve dy var eğer x sobel yapmak istiyorsan dx e 1 dy ye 0  ver

display(sobely)
# bu çıktılar farkedildiği üzere sobelx de yatay eksenler daha belirgin
# sobely de ise yataylar belirgin

lapplacian=cv2.Laplacian(image,cv2.CV_64F)# laplacianda ise hem yatayda hem dikeyde çizgiler daha belirgin

display(lapplacian)


#laplacianda elde ettiğimiz sonucu  hem yatayda hem dikeyde elde etmek için ise 

add=cv2.addWeighted(sobelx,0.5,sobely,0.5,gamma=0)# ağırlıklı ekleme ile sobel y ve xi aynı oranda birleştiririz

display(add)


ret,thresh=cv2.threshold(image,100,255,cv2.THRESH_BINARY)# 50 üstündeki pikselleri 255 e kalanı 0 a tamamlar

display(thresh)


kernel=np.ones((4,4),np.uint8)# morfoloji için kernel oluşturuldu
gradient=cv2.morphologyEx(add,cv2.MORPH_GRADIENT,kernel)# iki gradiantın birleştiği resimde içerdeki sayıların net görünmesi için gradiant morfoloji uygulanır

display(gradient)# burada farklı bir görüntü var amaç belirginleştirmek onu bilmen yeterli
