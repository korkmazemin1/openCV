from imutils.video import VideoStream
import argparse
import time
import cv2
import simple_detect_barcode as bar_det


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
args = vars(ap.parse_args())

if not args.get("video", False):
	vs = VideoStream(src=0).start()
	time.sleep(2.0)# eğer video yoksa webcami açar
else:
	vs = cv2.VideoCapture(args["video"])# video  verildi ise video kullanılır

while True:
	
    frame = vs.read()
    frame =frame[1] if args.get("video",False) else frame  #video okundu

    if frame is None:# vide bittiyse durdurur
        break

    box=bar_det.detect(frame)


    if box is not None :# barcode tespit edildi ise konturun etrafını çizer
          cv2.drawContours(frame,[box],-1,(0,255,0),2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF     


    if key == ord("q"):
        break

if not args.get("video", False):# video okuma bittiyse  durdur
    vs.stop()
else: 
    vs.release()# ya da webcami bırak


cv2.destroyAllWindows()       