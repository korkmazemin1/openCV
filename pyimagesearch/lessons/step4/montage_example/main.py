"""
Bu mini projede build_montages fonksiyonu ile resimleri sırası ile gösterdik

            ALGORİTMA


1-çektiğimiz resimleri shuffle ile karıştırdık           
2- komut satırından aldığımız resim yollarını for döngüsü ile haline getirdik   
3-build_montage ile sıralı bir şekilde gösterdik





"""




from imutils import build_montages
from imutils import paths
import argparse
import random
import cv2
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,help="path to input directory of images")
ap.add_argument("-s", "--sample", type=int, default=21,help="# of images to sample")
args = vars(ap.parse_args())

imagePaths=list(paths.list_images(args["images"]))# resimlerin yollarını liste haline 
random.shuffle(imagePaths)# yolları karıştırdık
imagePaths=imagePaths[:args["sample"]]# komut satırına yazılan sample ile kaç tane örnek gösterileceği belirtilir eğer belirtilmesse 21 adet gösterilir bakınız 28. satır
images=[]#liste açıldı

for imagePath in imagePaths:# bu döngü ile resimler sırası ile images listesine eklenir
    
    image=cv2.imread(imagePath)# resim okunur
    images.append(image)# listeye sondan eklenir
montages = build_montages(images,(150,300),(7,3))# montaj fonksiyonun ilk parametresi resimlerin listesi, ikincisi resimleri
# yeniden boyutlandırmamız gereken büyüklükler-- boş kısımlar siyah piksel ile tamamlanır-- üçüncü parametre ise 7 sütün ve 3 satır olduğunu belirtir


for montage in montages:
    cv2.imshow("Montage ",montage)
    cv2.waitKey(0)
now=datetime.now()
now=now.strftime('%Y_%m_%d_%H_%S')
cv2.imwrite(f"images/output/output_{now}.jpg",montage)    