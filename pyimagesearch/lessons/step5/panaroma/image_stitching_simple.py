from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,help="path to the output image")
args = vars(ap.parse_args())

print("[BİLGİLENDİRME] Resimler yükleniyor...")
imagePaths=sorted(list(paths.list_images(args["images"])))# çekilen resimleri listeleyip sıraladık
images =[]# liste dizisi tanımlandı

for imagePath in imagePaths:
    image =cv2.imread(imagePath)# döngü ile dönen resimler okundu
    images.append(image)# okunan resimler listelendi

print("[BİLGİLENDİRME] resimler birleştiriliyor")
stitcher =cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()# versiyon kontrolüne göre resimler dikma fonksiyonu farklı olarak çağrıldı
(status,stitched)=stitcher.stitch(images)# dikiş uygulandı

if status ==0:
    cv2.imwrite("images\\output\\{}".format(args["output"]),stitched)

    cv2.imshow("Stitched",stitched)
    cv2.waitKey(0)

else :
    print(f"[BİLGİLENDİRME] Resimleri birleştirme hata ile sonuçlandı ({status})")    
