"""
Bu mini projede nesnelerin belirlenen noktaları arasındaki uzaklık hesapları yapıldı

                ALGORİTMA
1-resim okundu
2-gray formata çevrildi
3-Gaussian blur yöntemi ile blur uygulandı
4-canny fonksiyonu ile kenarları saptandı
5-dilate ve erode fonksiyonları ile kenarlar arasındaki boşluklar kapatıldı
6-konturlar bulundu ve işlenebilir hale geldi
7-konturlar sıralandı
8-for döngüsü ile konturlar döndürüldü
9-yeteri kadar büyük olan konturların etrafını saracak olan dörtgenlerin özellikleri belirlendi
10-kutunun orta noktası bulundu
11-konturların etrafını saran dörtgenler çizildi
12-sol ve sağın orta noktaları hesaplandı
13-referans nesnenin öklid uzunluğu bulundu ve gerçek uzunluğu ile oranı hesaplandı
14-konturlar resmin üzerine çizildi
15-referans nesnesinin ve uzunluğu hesaplanacak diğer nesnenin kordinatları ayrı ayrı yığın haline getirildi
16-döngü içersinde iki nesnenin (referans ve diğeri) döngü ile sırası ile aynı noktalarına daireler ve aralarına çizgiler çekildi
17- her iki nokta arası mesafe sırası ile ekrana yazdırıldı





"""









from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime
now=datetime.now()


now=now.strftime('%Y_%m_%d_%H_%S')

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
colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0),
	(255, 0, 255))
refObj = None

for c in cnts :
    if cv2.contourArea(c)<100:# kontur yeterince büyük değilse görmezden gelinir -küçük parçaları atlamak için-
        continue
    
    box=cv2.minAreaRect(c)# bu fonksiyon ile tespit edilen nesnenin etrafını seran en küçük dörtgenin merkezi,eni ,boyu ve dönme açısı bulunur
    box=cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)# dörtgeni çizmek için ise minAreaRect den gelen bilgiler ile köşeler belirlenir
    box=np.array(box,dtype="int")# elde edilen veriler dizi haline gelir

    box=perspective.order_points(box)# noktaları sıralamak için hazırladığımız order_points fonksiyonunu çağırdık

    cX=np.average(box[:,0])
    cY=np.average(box[:,1])# x ve y  nin orta noktasını alarak kutunun merkezini bulduk


    if refObj is None:
        (tl, tr, br, bl) = box
        (tlblX, tlblY) = midpoint(tl, bl)# solda üst ve altın orta noktası
        (trbrX, trbrY) = midpoint(tr, br)# sağda üst ve altın orta noktası

        D=dist.euclidean((tlblX, tlblY), (trbrX, trbrY))# 
        refObj = (box, (cX, cY), D / args["width"])# burada kutunun sıralanmış noktaları , kutunun merkezi ve Öklid uzunluğu ile nesnenin gerçek uzunluğunun oranı oran hesaplamasında kullanılmıştır
        continue

    orig=image.copy()
    cv2.drawContours(orig,[box.astype("int")], -1, (0, 255, 0), 2)# kutular orijinal resmin üzerine çizildi
    cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2) 

    refCoords=np.vstack([refObj[0],refObj[1]])#referans nesnenin kordinatları yığına alındı
    objCoords=np.vstack([box,(cX,cY)])#diğer nesnenin kordinatları yığına alındı
    #nesnenin merkezini almak için yapıldı#########??????????

    for((xA,yA),(xB,yB),color) in zip(refCoords,objCoords,colors):
            cv2.circle(orig,(int(xA),int(yA)),5,color,-1)
            cv2.circle(orig,(int(xB),int(yB)),5,color,-1)
            #referans nesnesinin ve diğer nesnenin noktalarına daireler çizildi
            cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)),color, 2)# bu noktaların arasına çizgi çekildi

            D=dist.euclidean((xA,yA),(xB,yB))/refObj[2] #referansın ve diğer nesnenin arasındaki uzunluk hesaplandı#2 olarak gösterilen parametre öklid uzunluğu ile normal uzunluğun oranı 
            (mX, mY) = midpoint((xA, yA), (xB, yB))
            cv2.putText(orig, "{:.1f}in".format(D), (int(mX), int(mY - 10)),cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
            
            cv2.imshow("Image", orig)
            
            cv2.waitKey(0)
            cv2.imwrite(f"images/output/output_{now}.jpg",orig)