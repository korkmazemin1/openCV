import numpy as np 
import cv2
import argparse
from datetime import datetime

def color_transfer(source,target):
    source=cv2.cvtColor(source,cv2.COLOR_BGR2LAB).astype("float32")# color transfer yaparken negatif ve ondalık değerler olduğundan uint8 veritipi değil float32 ye geçilmiştir
    target=cv2.cvtColor(target,cv2.COLOR_BGR2LAB).astype("float32")# resimler sırası ile LAB formatına çevrildi

    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)# lab kanalarrının her biri için piksel yoğunluğunun ortalamasını ve standart sapmasını hesaplar
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    (l, a, b) = cv2.split(target)#cv2 split fonksiyonu kanal değerlerini tek tek çıkarır ve bunu (l,a,b) ye atadık
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar
    # kanal değerlerinde ortalamaları çıkardık
    
    
    l = ( lStdTar / lStdSrc ) * l
    a = ( aStdTar / aStdSrc ) * a
    b = ( bStdTar / bStdSrc ) * b
    #kanalları standart sapmaya göre ölçeklendirdik

    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc
    #laba kaynak kanallarının ortlamasını ekledik

    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)
    #0-255 in dışında kalan pikseller kırpıldı
    # dipnot: 0-255 opencv nin laba verdiği değerdir lab kanalları normalde 0-255 arasında değildir

    transfer=cv2.merge([l,a,b])# birleştirdiğimiz kanalları en son merge ile bir araya getirdik
    transfer=cv2.cvtColor(transfer.astype("uint8"),cv2.COLOR_LAB2BGR)#çıktı alacağımız görseli bgr formatına çevirdik

    return transfer


def image_stats(image):
	
	(l, a, b) = cv2.split(image)# l a b ayrıştırıldı
	(lMean, lStd) = (l.mean(), l.std())# l nin ortalaması ve standart sapması,
	(aMean, aStd) = (a.mean(), a.std())# a nin ortalaması ve standart sapması,
	(bMean, bStd) = (b.mean(), b.std())# b nin ortalaması ve standart sapması hesaplandı ve atandı

	return (lMean, lStd, aMean, aStd, bMean, bStd)

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,help="path to the input image")
ap.add_argument("-t", "--target", required=True,help="path to the input image")
args = vars(ap.parse_args())

now=datetime.now()
now=now.strftime('%Y_%m_%d_%H_%S')

image1=cv2.imread(args["source"])
image2=cv2.imread(args["target"])

transfer=color_transfer(image1,image2)

cv2.imshow("transfer",transfer)
cv2.imwrite(f"images/output/output_{now}.jpg",transfer)
cv2.waitKey(0)

"""



image=cv2.imread(color_transfer(args["source"],args["target"]))



cv2.imshow("color_transfer",image)
cv2.waitKey(0)
"""
