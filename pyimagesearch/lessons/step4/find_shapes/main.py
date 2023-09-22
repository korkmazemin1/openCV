"""

Resim üzerindeki siyah şekilleri saptayan mini projenin algortiması

1-resim okundu
2-saptanması gereken rengin alt ve üst değerleri atandı
3-inrange fonksiyonu ile sınırları verilen renk dışındaki değerler maskelendi
4-konutlar bulundu, liste haline getirildi
5-kaç tane şekil bulunduğu yazıldı
6-konturlar sırası ile resim üzerine çizildi ve ekrana gösterildi



"""


import numpy as np
import argparse
import imutils
import cv2
from datetime import datetime


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())
# komut satırı kodları

image=cv2.imread(args["image"])# resim okundu

lower=np.array([0,0,0])# istenen rengin minimum değerleri ve 
upper=np.array([15,15,15])# istenen rengin maksimum kanal değerleri dizi haline geldi
shapeMask=cv2.inRange(image,lower,upper)# alt ve üst sınırları belirtip inrange fonksiyonu ile tanımlamak istediğimi siyah renk dışında kalan kısımlar maskelendi

cnts=cv2.findContours(shapeMask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulunur
cnts=imutils.grab_contours(cnts)#konturlar sayısal formata çevriliyor

print(f"detectot found {len(cnts)} black shapes.")

now=datetime.now()
now=now.strftime('%Y_%m_%d_%H_%S')



for c in cnts:
    cv2.drawContours(image,[c],-1,(0,255,0),2)#konturlar çizilir
    cv2.imshow("image",image)
    cv2.imwrite(f"images/output/output_{now}.jpg",image)

    cv2.waitKey(0)