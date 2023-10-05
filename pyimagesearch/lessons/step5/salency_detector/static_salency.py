import argparse
import cv2
import cv2.saliency as sa

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

image=cv2.imread(args["image"])# resim okundu

saliency=sa.StaticSaliencySpectralResidual.create()# satitik belirginliği tespit eden fonksiyon
(success,saliencyMap)=saliency.computeSaliency(image)# resim içersinde belirgin alanlar çekildi
saliencyMap = (saliencyMap * 255).astype("uint8")# burada gray formatta 0-1 arasında 1 e yakın olanları ilgi çekici olarak belirler
cv2.imshow("Image", image)
cv2.imshow("Output", saliencyMap)
cv2.waitKey(0)


saliency = sa.StaticSaliencyFineGrained.create()# yukarıdakinden farklı bir fonksiyon ile belirgin alan bulunacak
(success, saliencyMap) = saliency.computeSaliency(image)# değerler üstteki fonksiyonun aksine 0-255 arası verilir

threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]# threshold uygulanır




