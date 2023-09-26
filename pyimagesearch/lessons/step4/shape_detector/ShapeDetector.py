"""
şekilleri tanımlayan  eden fonksiyonun algoritması
1-şeklin uzunluğunu bul
2-approxpolydp ile bozuk şekilleri düzelt
3-köşe sayılarını göre isimlendir ve isimi döndür



"""


import cv2


class ShapeDetector:
    def __init__(self) :
        pass

    def detect(self,c):# c parametresi tanımlamaya çalıştığımız şeklin konturlarını temsil eder

        shape="unidentified"
        peri=cv2.arcLength(c,True)#konturun uzunluğunu hesaplar
        approx=cv2.approxPolyDP(c,0.04*peri,True)# şekli bozuk olan kontuların şeklini düzeltmek için köşeler listesinde bizim verdiğimiz ikinci
        # parametre ile uzaklığını bizden alıp gereksiz köşeleri görmezden gelir mesela karenin üst kenarının ortasındaki bir köşeyi görmezden gelerek düz bir çizgi çeker


        if len(approx)==3:#eğer üç köşesi var ise üçgen olarak tanımlanır
            shape="triangle"
        elif len(approx)==4:# 4 köşesi var ise
            (x,y,w,h)=cv2.boundingRect(approx)
            ar=w/float(h)

            shape="square" if ar>= 0.95 and ar<= 1.05 else "rectangle"# kenarların uzunluğu kontrol edildi aynı ise kare değil ise dörtgen

        elif len(approx)==5:# 5 köşeli ise beşgen
            shape="pentagon"
        else :
            shape="circle"
        return shape