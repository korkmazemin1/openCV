from keyclipwriter import KeyClipWriter
from imutils.video import VideoStream

import argparse
import datetime
import imutils
import time
import cv2
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
ap.add_argument("-b", "--buffer-size", type=int, default=32,
	help="buffer size of video clip writer")
args = vars(ap.parse_args())


print("[BİLGİLENDİRME] Kamereya erişiliyor...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()# kamera seçimi
time.sleep(2.0)

whiteLower = (78, 154, 124)# tespit  edeceğimiz nesnenin hsv sınırları
whiteUpper = (138, 255, 255)

kcw = KeyClipWriter(bufSize=args["buffer_size"])# keyclip wirter başlatıldı
consecFrames = 0# eylem içermeyen kareler


while True:
    frame =vs.read()# kare okundu
    
    frame=imutils.resize(frame,width=600,height=600)# yeniden boyutlandırıldı
    updateConsecFrames=True# eylem içermeyen kareleri belirtme aktifleştirildi


    blurred = cv2.GaussianBlur(frame, (11, 11), 0)# blur uygulandı
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)# kareler hsv formatına çevrildi


    mask = cv2.inRange(hsv, whiteLower, whiteUpper)# tanımlanan sınırlar için mask uygulandı
    
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # küçük lekeleri ortadan kaldırmak için erode ve dilate fonksiyonları kullanıldı

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu
    cnts = imutils.grab_contours(cnts)# konturlar dizi haline getirildi

    

    if len(cnts) > 0:# kayda değer kontur var ise
		
        c = max(cnts, key=cv2.contourArea)# en büyük kontur alındı
        ((x, y), radius) = cv2.minEnclosingCircle(c)# konturun etrafını saracak en küçük çemberin verileri belirlendi
        updateConsecFrames = radius <= 10


        if radius >10: # eğer saptanan cisim kaydadeğer büyüklüğe sahip ise
            consecFrames=0# kayda değer bir görüntü olduğundan önemsiz görüntüler 0 olaraka atandı

            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)# saptanan cisme çember çizildi


            if not kcw.recording:# eğer kaydedilmeye başlanmadı ise kaydet
                timestamp=datetime.datetime.now()
                p="images\\output\\{}_{}.avi".format(args["output"],timestamp.strftime("%Y%m%d_%H%M%S"))#kaydedeceğimiz videonun kayıt yolu
                kcw.start(p, cv2.VideoWriter_fourcc(*"MJPG"),args["fps"])# video yazma

    if updateConsecFrames:
        consecFrames+= 1 # eğer herhangi bir hareket yoksa hareketsiz kareleri sayan sayacımız bir artar            

    kcw.update(frame)    

    if kcw.recording and consecFrames == args["buffer_size"]:# kayıt devam ediyorsa ve yeterli frame e ulaşışmıssa kayıt kapanır
        kcw.finish()

    cv2.imshow("Frame", frame)# kareler gösterilir
    key = cv2.waitKey(1) & 0xFF
    

    if key == ord("q"):
        break




if kcw.recording:# eğer başka bir kayıt açık ise
	kcw.finish()# kapat

cv2.destroyAllWindows()
vs.stop()