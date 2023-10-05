from skimage import transform
from skimage import filters
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image file")
ap.add_argument("-d", "--direction", type=str,
	default="vertical", help="seam removal direction")# resimin yatayda mı dikeyde mi kesileceği belirlenir
args = vars(ap.parse_args())

image = cv2.imread(args["image"])# resim okundu
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# gray formata çevrildi

mag = filters.sobel(gray.astype("float"))# enerji haritası için sobel gradyan gösterimi hesaplanır


cv2.imshow("Original",image)

for numSeams in range(20,140,20):# kaldırmak için sayıların üstünden geç
    
    carved=transform.seam_carve(image,mag,args["direction"],numSeams)

    print("[BİLGİLENDİRME]  {}  adet yer kaldırılıyor; yeni boyut: ""en={}, boy={}".format(numSeams, carved.shape[1],carved.shape[0]))
    

    cv2.imshow("kesilmis",carved)
    cv2.waitKey(0)

