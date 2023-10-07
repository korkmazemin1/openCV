import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image


array=np.array# dizi oluşturuldu
array=np.full((5,5),10)# boyutları belirlenip dizinin bütün elemanlarına 10 değeri verildi
print(array)


ran_array=np.random.randint(low=0,high=1200,size=(10,10))# rastgele 0-1200 arasında 10 satır ve sütunluk bir matrsi oluşturuldu
print(ran_array)
a=ran_array.max()# matrisin en büyük elemanı alındı
print(a)


image=Image.open("opencv_22\\step_2\\image.jpg")# görsel açıldı

plt.imshow(image)
plt.waitforbuttonpress()
image=np.asarray(image)# görsel dizi haline getirildi
image_red=image[:,:,0]# görselin kırmızı kanal değerleri atandı

plt.imshow(image_red)# kırmızı kanal  değerleri ile sadece kırmızı kanal gösterildi"
plt.waitforbuttonpress()