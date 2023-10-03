from __future__ import print_function
from basicmotiondetector import BasicMotionDetector
from panaroma import Stitcher
from imutils.video import VideoStream
import numpy as np
import datetime
import imutils
import time
import cv2


print("[BİLGİLENDİRME] Kamere başlatılıyor")

leftstream=VideoStream(src=0).start()
rightStream=VideoStream(src=1).start()# iki kamerada başlatıldı bu kodu src ile oynayarak ayrı bir kamera ile çalıştırabilirsin
time.sleep(2.0)


stitcher= Stitcher()
motion=BasicMotionDetector(minArea=500)
total=0

while True:
    left=leftstream.read()
    right=rightStream.read()# iki kameradan da görüntüler ayrı ayrı okundu

    result=stitcher.stitch([left,right])# kameralarının konumlarını keyfimize göre belirledik

    if result is None:# homografi bulunamadı ise
        print("[BİLGİLENDİRME] Homografi hesaplanamadı")
        break

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)# renk uzayı siyah beyaz formata çevrildi
    gray = cv2.GaussianBlur(gray, (21, 21), 0)# blur uygulandı
    locs = motion.update(gray)#hareket tespiti fonksiyonu çağrıldı

    if total >32 and len(locs)>0:# ilk 32 karede arka plan tespiti yapılır bu yüzden ilk 32 karede arkaplanda bir hareket olmamalıdır
        
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)
        # min max x ler  belirlenir
        
        for l in locs:
            (x,y,w,h)=cv2.boundingRect(l)# hareket saptanan konumların verileri çekildi
            (minX, maxX) = (min(minX, x), max(maxX, x + w))
            (minY, maxY) = (min(minY, y), max(maxY, y + h))


            cv2.rectangle(result, (minX, minY), (maxX, maxY),
			(0, 0, 255), 3)# tespit edilen harekete dörtgen çizildi
    
    total +=1# karelerin sayısı sayaç ile hesaplanır ve ->
    timestamp=datetime.datetime.now()
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")    # ekrana yazdırılır
    cv2.putText(result, ts, (10, result.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    cv2.imshow("Result", result)    
    cv2.imshow("Left Frame", left)
    cv2.imshow("Right Frame", right)
    key = cv2.waitKey(1) & 0xFF

    if key==ord("q"):
        break


print("[BİLGİLENDİRME] KAMERALARA KAPATILIYOR...")
cv2.destroyAllWindows()
leftstream.stop()
rightStream.stop()
    