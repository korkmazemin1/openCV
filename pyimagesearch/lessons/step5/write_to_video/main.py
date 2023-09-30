from __future__ import print_function
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=20,
	help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
	help="codec of output video")
args = vars(ap.parse_args())


print("[BİLGİLENDİRME] kamera  aciliyor ...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()# kameranın web mi rapsperry mi olduğu kontrol edilir
time.sleep(2.0)

fourcc = cv2.VideoWriter_fourcc(*args["codec"])# codec atandı
writer = None # yazıcı değişkeni belirlendi
(h, w) = (None, None)# yükseklik ve genişlik değişkenleri belirlendi
zeros = None

while True:
    frame =vs.read()#kare okundu
    frame = imutils.resize(frame,width=600)

    if writer is None:
        (h,w) = frame.shape[:2]
        writer =cv2.VideoWriter(args["output"],fourcc,args["fps"],(w * 2, h * 2),True)# video yazıldı
        zeros = np.zeros((h,w),dtype="uint8")#sıfırları aldığımız array
    
    (B, G, R) = cv2.split(frame)# kareyi kanallarına ayırır
    R = cv2.merge([zeros, zeros, R])# yalnızca kırmızı 
    G = cv2.merge([zeros, G, zeros])# yalnızca yeşil
    B = cv2.merge([B, zeros, zeros])# yalnızca mavi pikselleri alır

    output = np.zeros((h * 2, w * 2, 3), dtype="uint8")
    output[0:h, 0:w] = frame#sol üste orijinal görüntü
    output[0:h, w:w * 2] = R# sağ üste kırmızı
    output[h:h * 2, w:w * 2] = G# sağ alt yeşil
    output[h:h * 2, 0:w] = B# sol alta ise mavi kanal piksellerine sahip kare geldi
    writer.write(output)



    cv2.imshow("Frame", frame)
    cv2.imshow("Output", output)
    key = cv2.waitKey(1) & 0xFF
	
    if key == ord("q"):
        break


print("[BİLGİLENDİRME] pencereler kapatılıyor...")
cv2.destroyAllWindows()
vs.stop()
writer.release()


