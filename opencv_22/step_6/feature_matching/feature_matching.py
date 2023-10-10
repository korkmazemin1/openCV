import numpy as np 
import cv2
import matplotlib.pyplot as plt

kelogs=cv2.imread("images\\input\\kelogs.webp")
kelogs_raf=cv2.imread("images\\input\\kelogs_raf.jpg")# resimler okundu

def display(img,cmap="gray"):# aldığı resimi gray formatta gösteren fonksiyon
    fig=plt.figure(figsize=(12,10))# resim boyutu belirlenir
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")# gray formatta ekrana basıtırılır
    plt.waitforbuttonpress()

display(kelogs)  

  