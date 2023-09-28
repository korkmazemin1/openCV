"""
bu kod dosyasında iki farklı video okuma tipi karşılaştırılmıştır
ilk while döngüsünde okumaya başka classlara ayırmadan yalnızca while içinde işlem yapılmıştır
ikinci while döngüsünde ise kareleri ayrıca okuyan bir class çağrılmıştır ve ikinci while da açık bir şekilde daha iyi fps alındığı görülmüştür







"""





from __future__ import print_function
from FPS import FPS
from WebcamVideoStream import WebcamVideoStream 
# yukarıdaki iki sınıfı kendi yazdığım py dosyalarından  import ettim şu şekilde çağırmakta doğru olacaktır:
"""
from imutils.video import WebcamVideoStream
from imutils.video import FPS
"""
import argparse 
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,help="# of frames to loop over for FPS test")# döngğye alınacak kare sayısı
ap.add_argument("-d", "--display", type=int, default=-1,help="Whether or not frames should be displayed")# okunan görüntüleri gösterileceğine karar verilir
# displayi aktif hale getirmek iş yükünü arttırdığından fps i düşürür bunu test aşamaları dışında kullanmak gereksizdir

args = vars(ap.parse_args())

print("[BİLGİLENDİRME] kameradan kareler aliniyor...")
stream = cv2.VideoCapture(0)# direkt okuma
fps = FPS().start()

while fps._numFrames < args["num_frames"]:# belirtilen fps sayısı geçilmediği sürece devam et
    (grabbed,frame)= stream.read()# kare okunur
    frame= imutils.resize(frame,width=400)# okunan kare yeniden boyutlandırılır

    if args["display"] > 0:# karenin gösterilip gösterilmeyeceği sorgulanır
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

    fps.update()# bir sonraki kare  çekilir

fps.stop()# belirtilen frame sayısı bitince döngüden çıkılır ve okuma durdurulur

print("[BİLGİLENDİRME] gecen sure: {:.2f}".format(fps.elapsed()))
print("[BİLGİLENDİRME] yakasik. FPS: {:.2f}".format(fps.fps()))

stream.release()
cv2.destroyAllWindows()


print("[BİLGİLENDİRME]  kameradan kareler aliniyor...")
vs = WebcamVideoStream(src=0).start()# class kullanarak okuma
fps = FPS().start()

while fps._numFrames < args["num_frames"]:# belirtilen fps sayısı geçilmediği sürece devam et
	
	frame = vs.read()# kameradan gelen görüntüler okunuyor
	frame = imutils.resize(frame, width=400)# kare yeniden boyutlandırılıyor
	
	if args["display"] > 0:# karenin gösterilip gösterilmeyeceği kontrol ediliyor
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
	
	fps.update()# bir sonraki kare çekiliyor

fps.stop()# belirtilen frame sayısı bitince döngüden çıkılır ve okuma durdurulur
print("[BİLGİLENDİRME] gecen sure: {:.2f}".format(fps.elapsed()))
print("[BİLGİLENDİRME] yakasik. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()

cv2.destroyAllWindows()
vs.stop()