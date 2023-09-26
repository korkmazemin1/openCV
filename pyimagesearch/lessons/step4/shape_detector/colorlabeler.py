# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler :
    def __init__(self):
        colors=OrderedDict({
            "red":(255,0,0),
            "green":(0,255,0),
            "blue":(0,0,255)})
        
        self.lab=np.zeros((len(colors), 1, 3), dtype="uint8")#renkleri tutması için numpy ile bir alan açtık
        self.colorNames=[]# renk isimleri için olan dizeyi açtık
        for (i,(name,rgb)) in enumerate(colors.items()):# item sözlüğün elemanlarıdır# bu döngüde sözlük içersindeki renklerin isimler ve rgb kodları i ile numara edilir
            self.lab[i]=rgb# lab tipindeki renkler için açtığımız alan sırsasıyla renklerin rgb kodları alınır
            self.colorNames.append(name)# burada da renklerin isimleri için açtığımız diziye renklerin isimleri sırası ile alınır


        self.lab=cv2.cvtColor(self.lab,cv2.COLOR_RGB2LAB)# rgb kodlarını aldığımız renkleri lab formatına çevirdik    
    def label (self,image,c):
        mask=np.zeros(image.shape[:2],dtype="uint8")#mask lar için bir alan açtık
        cv2.drawContours(mask,[c],-1,255,-1)# konturlar açılan mask alanına çizildi
        mask=cv2.erode(mask,None,iterations=2)# maskın arka plan ile karışmaması için erode ile biraz aşındırıldı
        mean=cv2.mean(image,mask=mask)[:3]# lab kanallarının her biri için ortalama hesaplandı

        minDist=(np.inf,None)# şu ana kadar bulunan minimum mesafe?

        for (i,row) in enumerate(self.lab) :
            d=dist.euclidean(row[0],mean)# lab kanalları arasındaki mesafe atandı

            if d<minDist[0]:
                minDist = (d,i)# en küçük öklid mesafesini döndürmek için aldık

        return self.colorNames[minDist[1]]        