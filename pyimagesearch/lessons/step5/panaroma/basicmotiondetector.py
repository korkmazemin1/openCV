import imutils
import cv2

class BasicMotionDetector:
    def __init__ (self,accumWeight=0.5,deltaThresh=5,minArea=5000):
        self.isv2=imutils.is_cv2()
        self.accumWeight =accumWeight# kısa sürede hareket -motion- fazla ise yüksek değer girmek kullanışlıdır
        self.deltaThresh =deltaThresh# deltathreshın daha büyük değerlerinde daha az hareket daha küçük değerlerinde daha çok hareket algılayacak
        self.minArea = minArea# göz ardı edilecek küçük alanlar
        
        self.avg =None# ortalama görüntü başlatılır


    def update(self,image):
        locs=[]# konumların dizisi -list of loacatiosn-

        if self.avg is None :# eğer avg yok ise şuanki frameden avg yi elde ettik
            self.avg=image.astype("float")
            return locs    
        

        cv2.accumulateWeighted(image,self.avg,self.accumWeight)# ağırlık hesaplandı
        frameDelta=cv2.abadiff(image,cv2.convertScaleAbs(self.avg))# geçerli kare ile ortalama karenin farkı


        thresh=cv2.threshold(frameDelta,self.deltaThresh,255,cv2.THRESH_BINARY[1])#delta resmine threshold uygulandı
        thresh=cv2.dilate(thresh,None,iterations=2)# boşlukları doldurmak için dilate fonksiyonu uygulandı

        cnts=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulundu
        cnts=imutils.grab_contours(cnts)#konturlar dizi haline getirildi

        for c in cnts:
            if cv2.contourArea(c) >self.minArea:# eğer kontur minimum alanı aştıysa 
                locs.append(c)# konum listesin eklenir

        return locs        


