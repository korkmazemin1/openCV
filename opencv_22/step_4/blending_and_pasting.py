import  cv2
import numpy as np 
import matplotlib.pyplot as plt

img1=cv2.imread("opencv_22\\step_4\\image.jpg")# resim okundu
img2=cv2.imread("opencv_22\\step_4\\indir.png")

img1_rgb=cv2.cvtColor(img1,cv2.COLOR_BGR2RGB)
img2_rgb=cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)# fotolar bgr dan rgb ye çevrildi

plt.imshow(img1_rgb)
plt.waitforbuttonpress()
plt.imshow(img2_rgb)
plt.waitforbuttonpress()

print(img1_rgb.shape)# resimlerin boyutları yazıldı
print(img2_rgb.shape)

img1_rgb=cv2.resize(img1_rgb,(1200,1200))
img2_rgb=cv2.resize(img2_rgb,(1200,1200))# resimleri yeniden boyutlandırdık

blended=cv2.addWeighted(img1_rgb,0.5,img2_rgb,0.5,gamma=0)# karıştırmak istediğimiz iki resmi ve bu resimlerin hemen yanındaki parametreler ise yoğunluğunluklarını veririz

plt.imshow(blended)
plt.waitforbuttonpress()


large_img=cv2.resize(img1_rgb,(1200,1200))
small_img=cv2.resize(img2_rgb,(600,600))# büyük olan resmin üstüne bastırmak için yeniden boyutlandırdık

large_img[0:600,0:600]=small_img# büyük fotonun belirli piksellerini küçük fotoya eşitledik ve üstüne yapıştırmış olduk

plt.imshow(large_img)
plt.waitforbuttonpress()
roi=large_img[0:600,600:1200]

plt.imshow(roi)#range of interest bölgesini ayırdık
plt.waitforbuttonpress()

gray=cv2.cvtColor(small_img,cv2.COLOR_RGB2GRAY)# resim siyah beyaz formata çevrildi

mask_inv= cv2.bitwise_not(gray)# piksellerin siyah ve beyaz değerleri yer değiştirdi

plt.imshow(mask_inv,cmap="gray")
plt.waitforbuttonpress()

white_backround=np.full((600,600,3),255,dtype=np.uint8)# beyaz renkli bir arka plan 

bk=cv2.bitwise_or(white_backround,white_backround,mask=mask_inv) # bitwise or ile arka plan ayarlandı

plt.imshow(bk)
plt.waitforbuttonpress()
img2_rgb=cv2.resize(img2_rgb,(600,600))
fg=cv2.bitwise_or(img2_rgb,img2_rgb,mask=mask_inv)# ön plan ayarlandı

plt.imshow(fg)
plt.waitforbuttonpress()

final_roi=cv2.bitwise_or(roi,fg)#iki resim birleştirildi
plt.imshow(final_roi)
plt.waitforbuttonpress()


large_img=img1_rgb
small_img =final_roi

large_img[0:600,600:1200]=small_img # ayarladğımız bölgeyi büyük resmin içine aldık

plt.imshow(large_img)
plt.waitforbuttonpress()







