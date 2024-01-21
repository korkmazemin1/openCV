import cv2
import numpy as np 
import matplotlib.pyplot as plt
print("a")
#kamera ayaları

cap=cv2.VideoCapture(0)#webcam açıldı

#bir adet frame oku

ret,frame=cap.read()

if ret==False:
    print("uyarı")
  

#detection
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")#cascade dosyası okundu
face_rects=face_cascade.detectMultiScale(frame)# ilk çekilen kareden yüz tespiti yapılır

(face_x,face_y,w,h)=tuple(face_rects[0])#yüzün bölgeleri alındı

track_window=(face_x,face_y,w,h)#meanshift algoritmasının girdisi

#ROI
roi=frame[face_y:face_y+h,face_x:face_x+w]#roiye tespit edilen yüz kordinatlarıo tanımnlandı

hsv_roi=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)# hsv formatına çevrildi

roi_hist=cv2.calcHist([hsv_roi],[0],None,[180],[0,180])# takip algoritmasında histogramlar karşılaştırılacağı için histpgram alındı

cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

# takip için gerekli durdurma kriterleri 
#count

term_crit=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5, 1)
# 5 yineleme veya bir tane epsilon

while True:
    ret,frame=cap.read()
    if not ret :
        print("problem")
        break
    if ret:
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)# renk uzayı hsv ye değiştirildi
        print("a")
        dst=cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)#histogramı bir görntüde bulmak için kullanıyoruz
        # bu fonksiyonda onu hesaplıyor 
        #piksel karşılaştırma

        ret,track_window=cv2.meanShift(dst,track_window,term_crit)

        x,y,w,h=track_window
        img2=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),5)
        cv2.imshow("Takip",img2)

        if cv2.waitKey(1)  & 0xFF == ord ("q"):break
cap.release()
cv2.destroyAllWindows()










