"""
Nesnelerin boyutunu hesaplayan bu mini projenin algoritması

kordinat düzleminde iki noktanın orta noktasını bulan midpoint fonksiyonu yazıldı

1-resim okundu
2-gray formata çevrildi
3-Gaussian blur yöntemi ile blur uygulandı
4-canny fonksiyonu ile kenarları saptandı
5-dilate ve erode fonksiyonları ile kenarlar arasındaki boşluklar kapatıldı
6-konturlar bulundu ve işlenebilir hale geldi
7-konturlar sıralandı
8-for döngüsü ile konturlar döndürüldü
9-yeteri kadar büyük olan konturların etrafını saracak olan dörtgenlerin özellikleri belirlendi
10-noktaları sıralamak için imutilsdeki order_points fonksiyonu kullanıldı
11-konturların etrafını saran dörtgenler çizildi
12-sırası ile kenarlar boyanması gereken noktalar ile boyandı
13-kenarların orta noktaları hesaplandı
14-orta noktalara daireler çizildi
15-orta noktalar arasına çizgi çekildi
16-üst ve alt taraftaki orta noktaların uzaklığı öklüd yöntemi ile bulundu
17-referans aldığımız nesnenin boyutu ile beraber hesapladığımız öklid uzunluğu ile pixelspermetric oranı bulundu
18-hesaplanan uzunluklar ekrana yazıldı


"""





from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(ptA,ptB):
    return ((ptA[0]+ptB[0])*0.5,(ptA[1]+ptB[1])*0.5)# kordinat düzleminde 2 noktanın orta noktasını hesaplayan fonksiyon
###
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True,help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())
### komut satırı için gerekli kodlar 


image=cv2.imread(args["image"])# yolu belirtilen resim okunduo
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#resim gray formata çevrildi
gray=cv2.GaussianBlur(gray,(7,7),0)#resme blur uygulandı

# kenarlar arasındaki boşluğu kapatmak adına erezyon ve dilation kullanılır
edged=cv2.Canny(gray,50,100)#canny fonksiyonu ile kenar tespiti yapıldı
edged=cv2.dilate(edged,None,iterations=1)# dilate ile piksel grupları büyütüldü
edged=cv2.erode(edged,None,iterations=1)# erozyon ve dilate ile ana hatlar arasındaki boşluklar kapandı -erode gürültü engelleyen bir fonksiyondur-

cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulunur
cnts=imutils.grab_contours(cnts)#konturlar sayısal formata çevrilir

(cnts,_)=contours.sort_contours(cnts)# konturlar soldan sağa sıralandı
pixelsPerMetric=None #pixels per metric değerine none atandı


for c in cnts :
    if cv2.contourArea(c)<100:# kontur yeterince büyük değilse görmezden gelinir -küçük parçaları atlamak için-
        continue
    orig=image.copy()
    box=cv2.minAreaRect(c)# bu fonksiyon ile tespit edilen nesnenin etrafını seran en küçük dörtgenin merkezi,eni ,boyu ve dönme açısı bulunur
    box=cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)# dörtgeni çizmek için ise minAreaRect den gelen bilgiler ile köşeler belirlenir
    box=np.array(box,dtype="int")# elde edilen veriler dizi haline gelir

    box=perspective.order_points(box)# noktaları sıralamak için hazırladığımız order_points fonksiyonunu çağırdık
    cv2.drawContours(orig,[box.astype("int")],-1,(0,0,255))# konturları çevreleyen dörtgen çizildi

    for (x,y) in box:
        cv2.circle(orig,(int(x),int(y)),5,(0,0,255),-1)#konturları çevreleyen kutularınköşelerine ise kırmızı daireler eklendi

    (tl,tr,br,bl)=box
    (tltrX,tltrY)=midpoint(tl,tr)# üstte sağ ve solun orta noktası
    (blbrX, blbrY) = midpoint(bl, br)#altta sağ be solun orta noktası
    (tlblX, tlblY) = midpoint(tl, bl)# solda üst ve altın orta noktası
    (trbrX, trbrY) = midpoint(tr, br)# sağda üst ve altın orta noktası

    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)# hesapladığımız orta noktalara daire çizildi

    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)# orta noktaların arasına çizgi çizildi


    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))# üst ve alttaki orta noktaların birbirine olan uzaklığı hesaplandı

    if pixelsPerMetric is None:
        pixelsPerMetric=dB/args["width"]# referans aldığımızı nesnenin hesapladığımız öklid uzunluğu ve elle girdiğimiz bilinen uzunluğunun oranı ile pixelspermetric diğer hesaplamalarda da kullanılacak

    dimA=dA/pixelsPerMetric
    dimB=dB/pixelsPerMetric

    cv2.putText(orig, "{:.1f}in".format(dimA),(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}in".format(dimB),(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,0.65, (255, 255, 255), 2)
	
    cv2.imshow("Image", orig)
    cv2.waitKey(0)
