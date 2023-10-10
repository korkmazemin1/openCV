import matplotlib.pyplot as plt
import cv2
import numpy as np

image=cv2.imread("images\\input\\image.jpg")# resim okundu

edges=cv2.Canny(image,threshold1=127,threshold2=127)# canny tespit algoritmasında threshold değerleri optimize edilebilir

cv2.imshow("edges",edges)
cv2.waitKey()
cv2.destroyAllWindows()

blurred_img=cv2.blur(image,(3,3))# 5 e 5 lik bir kernel-çekirdekte- resime blur uygulandı
edges=cv2.Canny(blurred_img,100,180)# blurlanan resim canny algoritmasına çekildi

cv2.imshow("edged",edges)
cv2.waitKey()
cv2.destroyAllWindows()