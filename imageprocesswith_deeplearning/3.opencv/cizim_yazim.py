import numpy as np
import cv2

img=np.zeros((512,512,3),np.uint8)#sıfırlardan(siyah) oluşan bir resim oluşturuldu



cv2.line(img,(100,100),(200,200),(255,9,240),3)# resim üzerine bir çizgi çizildi



cv2.rectangle(img,(200,200),(300,300),(255,9,240),3)#dörtgen çizildi
cv2.circle(img,(350,350),66,(255,9,240),3)#çember çizildi
cv2.putText(img,"salam",(400,400),cv2.FONT_HERSHEY_SIMPLEX,1,(100,100,200))#yazı eklendi
cv2.imshow("siyah",img)
cv2.waitKey(0)
