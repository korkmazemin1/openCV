import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,help = "path to the image file")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])# resim okundu
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi

ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F# sürüm kontrolü yapıldı
gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)# gray formattaki görselin derinliğini gösteren gradyanın yatayda
gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)# ve dikeyde hesaplanması için gerekli büyüklükler

gradient = cv2.subtract(gradX,gradY)# iki gradyan arasındaki farklı kısımlara beyaz piksel atarak farkı ortaya çıkardık
gradient = cv2.convertScaleAbs(gradient)# sonuç 8 bite çevrildi

blurred = cv2.blur(gradient, (9, 9))# blur uygulandı
(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)# threshold uygulandı

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))# threshold sonucu barcode alanını roi yapabilmek için dikeydeki boşlukları kapama adına
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)# morfoloji işlemleri uygulandı

closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)#açıkta kalan boşlukları kapatmak adına dilate ve erode kullanıldı

cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu
cnts = imutils.grab_contours(cnts)# konturlar dizi haline getirildi
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]# konturlar alanlarına göre sıralandı

rect=cv2.minAreaRect(c)# konturun etrafını saran en küçük dörtgen belirlendi
box =cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
box = np.int0(box)


cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("Image", image)
cv2.waitKey(0)
