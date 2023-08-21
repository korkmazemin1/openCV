import numpy as np 
import argparse
import imutils
import cv2

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to the image file")
args=vars(ap.parse_args())

#   ^^^^^^resim yüklemek için gereken komut satırları ^^^^^^^^^^^
image=cv2.imread(args["image"])

for angle in np.arange(0,360,15):
    rotated=imutils.rotate(image,angle)#açtığımız döngü ile beraber 0-360 derece arası 15 derecelik değişimler ile resmi tek tek döndürdük
    cv2.imshow("Rotated",rotated)
    cv2.waitKey(0)

for angle in np.arange(0,360,15):
    rotated=imutils.rotate_bound(image,angle)#açtığımız döngü ile beraber 0-360 derece arası 15 derecelik değişimler ile resmi tek tek döndürdük
    cv2.imshow("Rotated",rotated)
    cv2.waitKey(0)

def rotate_bound(image,angle):
    (h,w)=image.shape[:2]# resmin en ve boyunu çektik
    (cX,cY)=(w//2,h//2)# en ve boya göre merkez kordinatlarını belirledik
    

    M=cv2.getRotationMatrix2D((cX,cY),-angle,1.0)# resmin  parametrelerde merkez ve dönme açısını verip dönme işlemleri uygulanmış matris elde ettik
    cos=np.abs(M[0,0])
    sin=np.abs(M[0,1])# cos ve sin değerleri belirlendi
    # bu değerler yeni resmin kesilmeden oluşacak en ve boyunu bulmamızı sağlar

    nW=int((h*sin)+(w*cos))
    nH=int((h*cos)+(w*sin))# cos ve sin kullanılarak yeni değerler hesaplandı

    M[0,2] += (nW/2)-cX
    M[1,2] += (nH/2)-cY# öteleme için ayarlar yapıldı

    return cv2.warpAffine(image,M,(nW,nH))


cv2.destroyAllWindows()
