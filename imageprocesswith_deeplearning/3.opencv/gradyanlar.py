import cv2
import numpy as np
from imshow import plt_imshow,plt_imshow_gray

""""
gradyan= görüntüdeki yoğunluk veya yönlü değişiklik

"""

img=cv2.imread("data\\sudoku(1).png")

# x gradyanları
sobelx=cv2.Sobel(img,ddepth=cv2.CV_16S,dx=1,dy=0,ksize=5)# kenar tespiti ile yalnızca dikey kenarları çıktı olarak verir
plt_imshow(sobelx)
#CV_16S parametresi yani derinlik parametresi piksellerin ne kadar detaylı olması gerektiğini belirtir 16 bit artı 16 bit eksi olur
# ayrıca 64 bit olanıda vardır bu hassasiyet ve bellek oranlarına göre optimal olanı belirlenir
# y gradyanları
sobelx=cv2.Sobel(img,ddepth=cv2.CV_16S,dx=0,dy=1,ksize=5)# kenar tespiti ile yalnızca dikey kenarları çıktı olarak verir
plt_imshow(sobelx)

#laplacian gradyanları
laplacian=cv2.Laplacian(img,ddepth=cv2.CV_16S)
plt_imshow(laplacian)
