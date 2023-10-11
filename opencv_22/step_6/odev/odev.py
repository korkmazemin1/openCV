import numpy as np
import cv2
import matplotlib.pyplot as plt


# bgr-rgb  display()

#haarcascade_russian_plate_number

#def detect_plate 
#kırmızı renginde dörtgen çiz
# plakayı blurla

car=cv2.imread("images/input/car.jpg")


plate_cascade=cv2.CascadeClassifier("haarcascade_russian_plate_number.xml") # cascade çekildi

def detect_plate(img):
    plate_img=img.copy()
    plate_recs=plate_cascade.detectMultiScale(plate_img)# plaka cascade ile tespit edildi

    for (x,y,w,h) in plate_recs:
        roi=plate_img[y:y+h,x:x+w]# plakanın alanı roiye çekildi
        cordinates=x,y,w,h# plakanın kordinatları atandı
        cv2.rectangle(plate_img,(x,y),(x+w,y+h),(0,0,255),7)#plakanın etrafına dörtgen çizildi
        
    return plate_img,roi,cordinates


result,roi,cordinates=detect_plate(car)# fonksiyon çalıştırıldı ve gerekli değerler çekildi


cv2.imshow("result",result)
cv2.imshow("roi",roi)
cv2.waitKey(0)
cv2.destroyAllWindows()

blur=cv2.blur(roi,(27,27))# plakanın bulunduğu alana blur uygulandı

cv2.imshow("blur",blur)
cv2.waitKey(0)
cv2.destroyAllWindows()

x,y,w,h=cordinates

car[y:y+h,x:x+w]=blur# blurlu plaka resme eklendi

cv2.imshow("blur_plat",car)
cv2.waitKey()
cv2.destroyAllWindows()





