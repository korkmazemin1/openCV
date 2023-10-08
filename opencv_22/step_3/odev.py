import cv2
import numpy as np
import matplotlib.pyplot as plt


image=cv2.imread("opencv_22\\step_3\\image.jpg")# resim okundu

image_rgb=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)# renk uzayı bgr dan rgb ye çevrildi

plt.imshow(image_rgb)# foto plt ile gösterildi
plt.waitforbuttonpress()

print(image.shape)

cv2.rectangle(image_rgb,(20,200),(450,660),(255,0,0),3)# belirlenen bir alana dörtgen çizildi

points=np.array([[120,250],[200,23],[333,200]],dtype=np.int32)# üçgen çizmek için nokta listesi oluşturuldu
cv2.polylines(image,[points],True,(255,0,0),3)# bgr ile olan görüntünün üzerine belirlediğimiz noktalarda bir üçgen çizildi

image_rgb=cv2.flip(image_rgb,1)# x ekseninde resim ters çevrildi
cv2.imshow("bgr_poly",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

plt.imshow(image_rgb)# foto plt ile gösterildi
plt.waitforbuttonpress()



