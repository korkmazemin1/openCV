import cv2
import numpy as np 
import matplotlib.pyplot as plt

image=cv2.imread("opencv_22\\step_4\\image.jpg")# resim okundu
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)# renk uzayı rgb ye çevrildi


plt.imshow(image)
plt.waitforbuttonpress()



image_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)# hsv formatına çevrildi
plt.imshow(image_hsv)
plt.waitforbuttonpress()

image_hsl=cv2.cvtColor(image,cv2.COLOR_BGR2HLS)# hsl formatına çevrildi
plt.imshow(image_hsl)
plt.waitforbuttonpress()







