import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="resim yolunu yaziniz")
	
args = vars(ap.parse_args())

image=cv2.imread(args["image"])
image=cv2.resize(image,(640,640))
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#resim bgr dan gray(siyah-beyaz) formata çekildi
gray=cv2.GaussianBlur(gray,(3,3),0)# (3,3) kernel ile blur uygulandı
edged=cv2.Canny(gray,20,100)# canny ile kenarlar ortaya çıktı

cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# kenarları saptandı
cnts=imutils.grab_contours(cnts)# saptanan kenarlar düzenlend,-sayısal olarak-

if len(cnts)> 0 :
    c=max(cnts,key=cv2.contourArea) # c en büyük alana sahip kenarı temsil eder 
    mask=np.zeros(gray.shape,dtype="uint8")
    cv2.drawContours(mask,[c],-1,255,-1)# en büyük alana sahip olan kenarın içini beyaz rengi ile doldurduk 
    
    (x,y,w,h)=cv2.boundingRect(c)#roı bölgesinin bölgesini belirledik
    imageROI=image[y:y+h,x:x+w]
    maskROI=mask[y:y+h,x:x+w]
    imageROI=cv2.bitwise_and(imageROI,imageROI,mask=maskROI)# hap bölgesinin roı sini çıkardık

    for angle in np.arange(0,360,15):
        rotated=imutils.rotate(imageROI,angle)
        cv2.imshow("dondurme--yanlis-",rotated)
        cv2.waitKey(0)#bu döngüde hapın kenarlarını kesik biçimde döndürdük


    for angle in np. arange(0,360,15):
        rotated=imutils.rotate_bound(imageROI,angle)
        cv2.imshow("dondurme-- dogru",rotated)
        cv2.waitKey(0)     # bu döngüde ise hapın tüm alanı kapsayarak döndürürüz

cv2.imshow("mask",mask)
cv2.waitKey(0)
cv2.destroyAllWindows()