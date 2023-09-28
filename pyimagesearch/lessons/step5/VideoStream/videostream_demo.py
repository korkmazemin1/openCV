from VideoStream import VideoStream

import datetime
import argparse
import imutils
import time
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()# rapsperrypi kamerası kullanılıp kullanılmayacağına girilen parametre ile bakıldı
time.sleep(2.0)# bekleme komutu

while True :
    frame=vs.read()# video stream classı ile beraber kare okundu
    frame = imutils.resize(frame,width=400)# görüntü yeniden şekillendirildi


    timestamp=datetime.datetime.now() 
    ts=timestamp.strftime("%A %d %B %Y %I:%M:%S%p")# video okunurkenki zaman alındı
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)# videonun üstüne zaman yazıldı

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()    # videstream ile okuma durduruldu
