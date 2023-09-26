"""
Şekilleri tespit edip tanımlayan mini projenin algpritması

1-resimi oku
2-yeniden şekillendir ve eski boyut/ yeni boyut oranını al
3-gri formata çevir
4-blur uygula
5-threshold uygula
6-konturları bul ve dizi haline getir
7-shapedetector adlı import ettiğimiz fonksiyonu başlat
8-for döngüsü ile önce konturun merkezini bul
9-shape detector ile her şekli teker teker tanımla


"""

from ShapeDetector import ShapeDetector
from colorlabeler import ColorLabeler
import argparse
import imutils
import cv2
from datetime import datetime


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to the input image")
args = vars(ap.parse_args())



image = cv2.imread(args["image"])# resimi yükle
resized = imutils.resize(image, width=300)# yeniden boyutlandır
ratio = image.shape[0] / float(resized.shape[0])#en sonda doğru oranlamak için ratio yu aldık



blurred = cv2.GaussianBlur(resized, (5, 5), 0)# blur uygulandı
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
lab=cv2.cvtColor(blurred,cv2.COLOR_BGR2LAB)#renk tespiti için görselin kanalları bgr dan laba çevrildi

thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)[1]#threshold uygılandı


cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulundu
cnts = imutils.grab_contours(cnts)#konturlar dizi haline getirildi
sd = ShapeDetector()#  şekil tespiti için hazırladığımız fonksiyon import edildikten sonra başlattık
cl=ColorLabeler()#renk tespiti için hazırladığımız fonksiyon import edildikten sonra başlattık

for c in cnts:
    M = cv2.moments(c)
    cX=int(M["m10"]/ (M["m00"]+ 1e-7)*ratio)
    cY=int(M["m01"]/(M["m00"]+ 1e-7)*ratio)# moments kullanarak merkez hesaplandı
    shape = sd.detect(c)
    color = cl.label(lab, c)# iki fonksyinada parametreli verildi

    c=c.astype("float")
    c *=ratio
    c =c.astype("int")
    text = f"{color}  {shape}"
    cv2.drawContours(image,[c],-1,(0,255,0),2)# konturları doğru çizmek için başta aldığımız oranı konturların çiziminde kullandık
    cv2.putText(image, text, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)


    now=datetime.now()
    now=now.strftime('%Y_%m_%d_%H_%S')

    cv2.imwrite(f"images/output/output_{now}.jpg",image)
    cv2.imshow("Image", image)
    cv2.waitKey(0)