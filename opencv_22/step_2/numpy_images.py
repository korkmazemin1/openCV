import numpy as np 
import matplotlib.pyplot as plt    # çizim kütüphanesi

from PIL import Image #pıl=py image library

image= Image.open("opencv_22\\step_2\\image.jpg")

t=type(image)# açılan resmin tipi yazıldı
image_ar=np.asarray(image)

print(t)
print(image_ar.shape)# görselin şekilleri yazdırıldı

plt.imshow(image_ar)# görsel  gösterildi
plt.waitforbuttonpress()# herhangi bir tuşa basana kadar açık kal

channel_red=image_ar[:,:,0]# resmin yalnızca kırmızı renk kanal pikseli atandı
channel_green=image_ar[:,:,1]# yeşil kanal için
print(channel_red)

plt.imshow(channel_red)
plt.waitforbuttonpress()
plt.imshow(channel_red,cmap="gray")# kırmızı noktaların piksel değerlerini gray formatta gösterir
plt.waitforbuttonpress()
plt.imshow(channel_green)
plt.waitforbuttonpress()