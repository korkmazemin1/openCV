import numpy as np 
import cv2
import matplotlib.pyplot as plt


kelogs=cv2.imread("data\\kelogs.webp",0)# resim gray formatta okundu
kelogs_raf=cv2.imread("data\\kelogs_raf.jpg",0)# resimler okundu

sift=cv2.SIFT_create()# fonksiyonumuzu  başlattık

kp1, dist1 = sift.detectAndCompute(kelogs,None)# keypointleri ve tanımlayıcıları iki foto içinde aldık
kp2, dist2 = sift.detectAndCompute(kelogs_raf,None)# None parametresi mask kullanmamak için yapıldı

bf = cv2.BFMatcher()
matches=bf.knnMatch(dist1,dist2,k=2)# k=2 değeri ile en iyi ilk 2 matchi seçmek istediğimizi belirttik

good=[]

for match1,match2 in matches: # eşleşmeleri 1 ve 2. si olarak döndürürüz
    if match1.distance <0.75*match2.distance: # match 2 nin mesafesinin yüzde 75 i 1 inkinden büyükse# burada mesafe olarak kastedilen şey benzerlik oranıdır
        good.append([match1])# birinciyi iyi eşleşme listesine atarız


cizdirme2=cv2.drawMatchesKnn(kelogs,kp1,kelogs_raf,kp2,good,None,flags=2)# None  ile mask kullanmak istemediğimizi flags=2 ise default

cv2.imshow("cizdirme",cizdirme2)# ekran çıktılarında daha sağlam eşleşme elde ettiğimiz görülür

cv2.waitKey()