from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np 
import argparse 
import cv2
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "taranacak resmin yolu")
	       
args = vars(ap.parse_args())

#^^^komut satırı işlemleri^^^

image=cv2.imread(args["image"])# yolu verilmiş görüntü okundud
ratio=image.shape[0]/500.0 # resmin oranı tespit edildi
orig=image.copy()# resmin orijinal hali korundu
image=imutils.resize(image,height=500)# yüksekliğe 500 değeri verildi

# yukarıdaki işlemlerde resmin kenar algılamadaki doğruluğunu arttırmak için yüksekliği 500 yaptık ve oranladık

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
gray=cv2.GaussianBlur(gray,(5,5),0)# resmin bluru alındı
edged=cv2.Canny(gray,75,200)# canny fonksiyonu ile kenar tespiti yapıldı

print("ADIM 1: kenar tespiti")
cv2.imshow("Image",image)
cv2.imshow("EDGED",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

cnts=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)# kenarları tespit edilmiş görüntüden konturlar elde edildi
cnts=imutils.grab_contours(cnts)# konturlar veri olarak düzenlendi
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)[:5] # konturları alana göre sıraladık ve yalnızca en büyük olanları aldık

for c in cnts :
    peri=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*peri,True)# bu döngü ile beraber konturların sırası ile kenar sayısına bakılır

    if len(approx)==4: # ve  eğer 4 kenarlı bir kontur saptanırsa dögü kesilir ve o konturlar işleme devam edilir
        screenCnt=approx
        break

print("ADIM 2 :kagittan köşeler bulundu")    

cv2.drawContours(image,[screenCnt],-1,(0,255,0),2)# bulunan kenarları çizer
cv2.imshow("Outline",image) 
cv2.waitKey(0)
cv2.destroyAllWindows()


warped=four_point_transform(orig,screenCnt.reshape(4,2)*ratio)# transform.py de yaptığımız perspektif düzeltme fonksiyonu ile roi alanı düzgün bir biçimde görüntülenir

warped=cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)# gray formata çevrildi
T=threshold_local(warped,11,offset=10,method="gaussian")# threshold uygulandı
warped=(warped>T).astype("uint8")*255

print("ADIM 3 : perspektif dönüşümü yapildi")
cv2.imshow("orijinal",imutils.resize(orig,height=650))
cv2.imshow("taranmiş",imutils.resize(warped,height=650))
cv2.waitKey(0)