import numpy as np
import cv2
import matplotlib.pyplot as plt

image1=cv2.imread("data\\manzara1.jpg")
image2=cv2.imread("data\\manzara2.jpg")# resimler okundu
image1=cv2.cvtColor(image1,cv2.COLOR_BGR2RGB)
image2=cv2.cvtColor(image2,cv2.COLOR_BGR2RGB)# resimleri plt ile görselleştirebilmek için bgr dan rgb formatına çevirdik
image1=cv2.resize(image1,(600,600))
image2=cv2.resize(image2,(600,600))# karıştırmak için aynı boyutlara getirdik


plt.figure()
plt.imshow(image1)
plt.waitforbuttonpress()
plt.figure()
plt.imshow(image2)
plt.waitforbuttonpress()

blended_image=cv2.addWeighted(src1=image1,alpha=0.5,src2=image2,beta=0.5,gamma=0)# bu fonksiyon alpha*img1+alpha*img2 işlemi ile resimleri karıştırır alpha ve beta katsayılarını biz belirleyeceğiz
# alpha ve beta katsayıları ile oynayarak istediğin miktarda karıştırabilirsin# gamma arttıkça parlaklık artıyor
plt.figure()
plt.imshow(blended_image)
plt.waitforbuttonpress()