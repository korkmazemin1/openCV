from imshow import plt_imshow,plt_imshow_gray
import numpy as np
import cv2

image=cv2.imread("data\\team.png",0)# resim okundu

plt_imshow_gray(image)

#erozyon sınırları küçültür


kernel=np.ones((5,5),dtype=np.uint8)# integer 5 e 5 bir matris
erode=cv2.erode(image,kernel,iterations=1)# 1 tekrarlı bir erezyon işlemi uygulandı

plt_imshow_gray(erode)

dilation=cv2.dilate(image,kernel,iterations=1)# dilate işlemi ile sınırlar büyütüldü

plt_imshow_gray(dilation)


white_noise = np.random.randint(0,2,size=image.shape[:2])#image shapede sadece 0 ve 1. elemanlar  alınrak kanal değeri atlanmıştır

white_noise=white_noise*255# bizim renk skalasına çevrildi

plt_imshow_gray(white_noise)

noise_img=white_noise+image# beyaz kiri ve fotoyu birleştirerek resmimizi kirli bir hale getirdik

plt_imshow_gray(noise_img)

opening=cv2.morphologyEx(noise_img.astype(np.float32),cv2.MORPH_OPEN,kernel)# gürültülü görseli erezyon ve dilatein sırası ile uygulanması ile kirleri giderdi
# önce beyazlar açıldı sonra arttırıldı ve kirli görseller giderildi
plt_imshow_gray(opening)

black_noise = np.random.randint(0,2,size=image.shape[:2])#image shapede sadece 0 ve 1. elemanlar  alınrak kanal değeri atlanmıştır

black_noise=black_noise*-255# bizim renk skalasına çevrildi

plt_imshow_gray(black_noise)

black_noise_img=black_noise+image
black_noise_img[black_noise_img <= -245] = 0# siyah kir için filtre
plt_imshow_gray(black_noise_img)
closing =cv2.morphologyEx(noise_img.astype(np.float32),cv2.MORPH_CLOSE,kernel)# siyah kir içinse az önce yapılan işlemin tersi yapıldı ve siyah kir giderildi

plt_imshow_gray(closing)


gradient =cv2.morphologyEx(image,cv2.MORPH_GRADIENT,kernel)# şekillerin içleri boşaldı ve sadece kenarları kaldı

plt_imshow(gradient,"gradient")
