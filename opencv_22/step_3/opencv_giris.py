import numpy as np
import cv2
import matplotlib.pyplot as plt

img=cv2.imread("opencv_22\\step_3\\image.jpg")# resmin yolu girilerek okundu

print(type(img))# resmin tipi yazıldı

print(img.shape)# resmin boyutları yazıldı

plt.imshow(img)# matplotlib ile gösterdik
# Matplotlib RGB opencv ise BGR ile resimleri okur bu nedenle opencv ile okunmuş görseli şekildeki gibi matplotlib ile gösterirsek kanallar farklı gözükür
plt.waitforbuttonpress()
new_i=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(new_i)
plt.waitforbuttonpress()

img_gray =cv2.imread("opencv_22\\step_3\\image.jpg",cv2.IMREAD_GRAYSCALE)# resmi siyah beyaz şekilde okuduk
print(img_gray.shape)

cv2.imshow("gray",img_gray)
cv2.waitKey(0)


plt.imshow(img_gray,cmap="gray")#plt ile resmi okurken color mapi belirtmemiz gerekir aksi takdirde RGB olarak okur
plt.waitforbuttonpress()

plt.imshow(img_gray,cmap="magma")# farklı bir colormap kullanıldı
plt.waitforbuttonpress()

resize_img=(img,(600,600))
cv2.imshow("resize",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
w_ratio=0.5
h_ratio=0.5# en ve boyun yarısı alınarak foto yeniden boyutlandırıldı

new_img=cv2.resize(img,(0,0),img,w_ratio,h_ratio)# en boy oranını belirterek resize ettik

flipy_img=cv2.flip(img,0)# fotoğrafı y ekseninde ters çevirdik
flipx_img=cv2.flip(img,1)# fotoğrafı x ekseninde ters çevirdik
flipxy_img=cv2.flip(img,-1)# fotoğrafı x ve y eksenlerinde döndürdük

cv2.imshow("flipy",flipy_img)
cv2.imshow("flipx",flipx_img)
cv2.imshow("flipxy",flipxy_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("opencv_22\\step_3\\new_image.jpg",flipxy_img)


while True:
    cv2.imshow("img",img)

    if cv2.waitKey(1) & 0xFF ==27:# Esc tuşuna basana kadar fotoğraf açık kalır
        break
cv2.destroyAllWindows()    
