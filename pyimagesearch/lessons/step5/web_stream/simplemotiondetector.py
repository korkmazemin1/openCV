import numpy as np
import imutils
import cv2


class SingleMotionDetector:
    
    def __init__(self,accumWeight=0.5):# birikimli ağırlığı ön arka eşit şekilde 0.5 alındı bu değer farklı projelerde değişkenlik gösterebilir
        self.accumWeighted =accumWeight# birikmiş ağırlık açıldı
        #accumWeight  ne kadar büyük ise arkaplan ağırlık hesaplamada o kadar az çıkar
        self.bg =None # arkaplan değişkeni açıldı

    def update(self,image):
        if self.bg is None :
            self.bg =image.copy().astype("float")# eğer arka plan yoksa aç

        cv2.accumulateWeighted(image,self.bg,self.accumWeighted)# arka planı birikimli ağırlık ile güncelle

    def detect(self,image,tVal=25):
        delta=cv2.absdiff(self.bg.astype("uint8"),image)#  resim ve arka plan arasındaki mutlak fark hesaplanır
        thresh=cv2.threshold(delta,tVal,255,cv2.THRESH_BINARY)[1]# threshold uygulandı
        # piksel değeri 25 den büyük olanlar 255 olarak ayarlanır
        thresh=cv2.erode(thresh,None,iterations=2)
        thresh=cv2.dilate(thresh,None,iterations=2)# dilate ve erode küçük lekeleri kaldırmak için uygulandı

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# threshli görüntüden kontur tespiti yapıldı
        cnts = imutils.grab_contours(cnts)# tespit edilen konturlar dizi haline getirildi

        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)# hareketin olduğu konumdaki dörtgenin konum tespitleri

        if len(cnts) == 0:
            return None# kontur tespit edilemedi ise none değeri döner
        
        for c in cnts:

            (x,y,w,h)=cv2.boundingRect(c)# tespit edilen karenin değerleri alınır
            (minX,minY) = (min(minX,x),min(minY,y))
            (maxX,maxY) = (max(maxX,x+w),max(maxY,y+h))# hareket tespit edilen bölgenin max x ve y si 
        return (thresh,(minX,minY,maxX,maxY))






