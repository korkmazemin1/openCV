

""""
                    -+++ALGORİTMA+++-

kütüphaneler eklendi
resim yüklemek için komut satırı kodları yazıldı
saptanması gereken renklerin rgb formdakl alt ve üst (lower-upper ) değerleri liste halinde girildi 
for döngüsü rgb değerlerini renk renk alacak şekilde açıldı 
rgb sınır değerleri "uint8" formatına çevrildi
sınır değerlerine göre mask uygulandı
uygulanan bitwise işleçleri ile uygulanan mask bölgelerinde saptanan renk bölgeleri beyaz diğer bölgeler siyah piksel olarak tanımlandı
son olarak np.hstack ile girdi ve çıktılar satırda sıra ile yan yana gösterildi



"""
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "resmin yolu")
args = vars(ap.parse_args())# resmi yüklemek için gerekli komut satırları

image = cv2.imread(args["image"])

boundaries=[
    ([17, 15, 100], [50, 56, 200]),
	([86, 31, 4], [220, 88, 50]),
	([25, 146, 190], [62, 174, 250]),#> renk tespiti için renklerin alt ve üst değerleri (lower-upper)
	([103, 86, 65], [145, 133, 128])
]
for (lower,upper) in boundaries:
    lower=np.array(lower,dtype="uint8")
    upper=np.array(upper,dtype="uint8")# değerler için numpy ile dizi oluşturduk

    mask=cv2.inRange(image,lower,upper)# rgb formatında alt ve üst değerler arasındaki pikseller masklandı
    output=cv2.bitwise_and(image,image,mask=mask)# mask ile saptanan renkleri beyaza diğer pikselleri siyaha boyadık

    cv2.imshow("images",np.hstack([image,output]))# hstack fonksiyonu ouput ile image i satır bazında yan yana dizdi yani orijinal resmi ve renk saptama çıktısını yan yana görebiliriz
    cv2.waitKey(0)
    cv2.destroyAllWindows()