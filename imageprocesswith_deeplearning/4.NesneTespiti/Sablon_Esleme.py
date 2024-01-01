import numpy as np 
import cv2
from imshow import plt_imshow,plt_imshow_gray
import matplotlib.pyplot as plt

image=cv2.imread("data\\messi.jpg")
template=cv2.imread("data\\messim.png")
h,w = template.shape[:-1]
methods =['cv2.TM_CCOEFF','cv2.TM_CCOEFF_NORMED','cv2.TM_CCORR','cv2.TM_CCORR_NORMED','cv2.TM_SQDIFF','cv2.TM_SQDIFF_NORMED']

for meth in methods:
    method=eval(meth)# stringleri fonksiyona çevirdik
    res=cv2.matchTemplate(image,template,method)# şablon eşleştirme yapıldı

    min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(res)# sonuçun minimum ve maksimum kordinatları alınır

    if method in ['cv2.TM_SQDIFF','cv2.TM_SQDIFF_NORMED']:# metodların çıktısı farklı olduğundan koşul eklendi
        top_left =min_loc# min loc  sol üste denk gelir
    else:
        top_left=max_loc    

    bottom_right=(top_left[0]+w,top_left[1]+h)
    cv2.rectangle(image,top_left,bottom_right,255,2)

    plt.subplot(1, 2, 1)
    plt.imshow(res, cmap="gray")
    plt.title("eşleşen sonuç")

    plt.subplot(1, 2, 2)
    plt.imshow(image, cmap="gray")
    plt.title("tespit edilen sonuç")

    plt.show()








