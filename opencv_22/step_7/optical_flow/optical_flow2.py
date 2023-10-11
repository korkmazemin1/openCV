import numpy as np 
import cv2

cap=cv2.VideoCapture(0)# webcama erişildi


ret,frame1=cap.read()

prvsImg=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)# renk uzayı gray formata çevrildi

hsv_mask=np.zeros_like(frame1)# gerçek framein boyutunda her pikseli sıfır olan bir np arrayi oluşturdu

hsv_mask[:,:,1]=255 # x y ve 2. renk kanalının 255 e eşitledik

while True:
    ret,frame2=cap.read()

    nextImg=cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)# frame gray formata çevrildi
    

    flow=cv2.calcOpticalFlowFarneback(prvsImg,nextImg,0.5,3,15,3,5,1.2,0)# karelerimizi ve default parametrelerini girdik
    # flow çıktısını ise :

    mag,ang=cv2.cartToPolar(flow[:,:,1],flow,angleInDegrees=True)#fllowun x ye ve ikinci kanalını aldık
    # bu fonksiyon iki boyutlu vektörlerin büyüklüklerini ve açılarını hesaplıyor

    hsv_mask[:,:,0]= ang/2 # maskenin kordinatlarına açı entegre edilir
    hsv_mask[:,:,2]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

    BGR=cv2.cvtColor(hsv_mask,cv2.COLOR_HSV2BGR)# renk uzayı bgr a döndü

    cv2.imshow("frame2",BGR)

    k=cv2.waitKey(30) & 0xFF
    if k==27:
        break

    prvsImg=nextImg# döngüyü tamamlamak adına eşitleme işlemi

cap.release()
cv2.destroyAllWindows()        





    






