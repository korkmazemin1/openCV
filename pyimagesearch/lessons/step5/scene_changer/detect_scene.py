import argparse
import imutils
import cv2
import os


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, type=str,
	help="path to input video file")
ap.add_argument("-o", "--output", required=True, type=str,
	help="path to output directory to store frames")
ap.add_argument("-p", "--min-percent", type=float, default=1.0,
	help="lower boundary of percentage of motion")
ap.add_argument("-m", "--max-percent", type=float, default=10.0,
	help="upper boundary of percentage of motion")
ap.add_argument("-w", "--warmup", type=int, default=200,
	help="# of frames to use to build a reasonable background model")
args = vars(ap.parse_args())

fgbg = cv2.bgsegm.createBacgroundSubtractorGMG()# arka plan çıkarıcı oluşturuldu


catured=False # belirli bir çerçevenin oluşup oluşmadığını kontrol eden bool
total=0# toplam frame sayısı
frames=0# işlem görmüş frame sayısı

vs=cv2.VideoCapture(args["video"])# video için alan açıldı
(W,H)=(None,None)


while True:
    (grabbed,frame)=vs.read()

    if frame is None:# frame yok ise video bitmiş demektir
        break

    orig=frame.copy()# kare korundu
    frame =imutils.resize(frame,width=600)   # yeniden boyutlandırıldı
    mask =fgbg.apply(frame)# arka plan çıkarıcı uygulandı

    mask =cv2.erode(mask,None,iterations=2)
    mask=cv2.dilate(mask,None,iterations=2) # gürültü gidermek adına erode ve dilate fonksiyonları uygulandı

    if W is None or H is None :
        (H,W) = mask.shape[:2]# en boy boş ise arka plan çıkarılmış olan resimden alınır

    p = (cv2.countNonZero(mask)/float(W*H))*100 # önplanın yüzdesi hesaplanır

    if p < args["min_percent"] and not captured and  frames > args["warmup"]:# eğer belirlenen yüzdeyi geçtiyse hareket durduğu anlaşılır ve frame alınır
        cv2.imshow("captured",frame)# ayrıca gösterilir
        captured =True  

        filename = "{}.png".format(total)# kare için isim
        path = os.path.sep.join([args["output"], filename])# kare için path yapıldı
        total += 1 # ve toplam toplanan kare sayısı arttırıldı

        print("[INFO] saving {}".format(path))
        cv2.imwrite(path, orig)
    elif captured and p >= args["max_percent"]:# sahne hareket halinde ise sahne durana kadar beklenir 
	   
        captured = False
         

    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1) & 0xFF
	
    if key == ord("q"):
        break
	
    frames += 1

vs.release()     