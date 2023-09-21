"""
 şekillerin merkezini hesaplayan mini projenin algoritması:
 1-resimi oku
 2-gray formata çevir
 3-blur uygula
 4-threshold uygula
 5-konturları sapta ve işlenebilir hale getir
 6-for döngüsü ile moments fonksiyonu ile beraber merkezin kordinatlarını hesapla
 7-konturları ve merkezi gösterecek çemberi çiz



"""

import argparse
import imutils
import cv2
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to the input image")
args = vars(ap.parse_args())

#komut satırı için gerekli kodlar

image=cv2.imread(args["image"])# resim okundu
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
blurred=cv2.GaussianBlur(gray,(5,5),0)# blur uygulandı
thresh=cv2.threshold(blurred,60,255,cv2.THRESH_BINARY)[1]#threshold uygulandı--ikinci parametre threshold değeri üçüncü ise maksimum değer
#cv2.imshow("tehresh",thresh)
#cv2.waitKey(0)

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulunur
cnts=imutils.grab_contours(cnts)#konturlar sayısal formata çevriliyor



for c in cnts:
    M=cv2.moments(c)
    print(M["m00"])
    print(M["m01"])
    print(M["m10"])
    cX=int(M["m10"]/ (M["m00"]+ 1e-7))
    cY=int(M["m01"]/(M["m00"]+ 1e-7))

    #moments kullanılarak konturun merkezi hesaplandı

    cv2.drawContours(image,[c],-1,(0,255,0),2)# konturlar çizildi
    cv2.circle(image,(cX,cY),7,(255,255,255),-1)# bulduğumuz merkeze daire çizdik



    now=datetime.now()
    now=now.strftime('%Y_%m_%d_%H_%S')
    cv2.imwrite(f"images/output/output_{now}.jpg",image)
    cv2.imshow("image",image)
    cv2.waitKey(0)
