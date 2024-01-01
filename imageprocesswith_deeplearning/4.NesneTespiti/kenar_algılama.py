import cv2
import numpy as np
from imshow import plt_imshow,plt_imshow_gray
import matplotlib.pyplot as plt


image=cv2.imread("data\\car.jpg")
cv2.imshow("image",image)
cv2.waitKey()

edges=cv2.Canny(image,threshold1 =0 , threshold2 = 255)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# thresold uygulanmadığında girinti ve çıkıntı dahil tüm kenarları aldı
cv2.waitKey()

median_value=np.median(image)# optimal threshold için medin değeri çekildi
print(median_value)

low=int(max(0,(1-0.33)*median_value))
high=int(max(0,(1+0.33)*median_value))
edges=cv2.Canny(image,threshold1 =low , threshold2 = high)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# kursta optimal olduğu belirtilen threshold parametreleri işe yaramadı
cv2.waitKey()
median_value=np.median(image)# optimal threshold için medin değeri çekildi
print(median_value)

low=int(max(0,(1-0.33)*median_value))
high=int(max(0,(1+0.33)*median_value))
blurred=cv2.blur(image,(5,5))
edges=cv2.Canny(image,threshold1 =low,threshold2 = high)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# kursta optimal olduğu belirtilen threshold parametreleri işe yaramadı
cv2.waitKey()#median value yönteminin pek bir işe yaramadığı gözlemlendi