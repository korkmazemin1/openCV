import cv2
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import time
import argparse

OPENCV_OBJECT_TRACKERS =  {"csrt":cv2.legacy.TrackerCSRT.create,
                              "kcf":cv2.legacy.TrackerKCF.create,
                              "boosting":cv2.legacy.TrackerBoosting.create,
                              "mil":cv2.legacy.TrackerMIL.create,
                              "tld":cv2.legacy.TrackerTLD.create,
                              "medianflow":cv2.legacy.TrackerMedianFlow.create,
                              "mosse":cv2.legacy.TrackerMOSSE.create}# takip algoritmaları sözlük hali ile sıralandı
print("algoritmalar: \n csrt \n kcf \n boosting \n mil \n tld \n medianflow \n mosse  ")
algorithm=input("lütfen kullanmak istediğiniz algoritmayi seçiniz:")
 
trackers=cv2.legacy.MultiTracker.create()

video_path="coklu_takip_vid.mp4"

cap=cv2.VideoCapture(video_path)

fps=30
f=0

while True:
    ret,frame=cap.read()
    if ret:
        frame=cv2.resize(frame,dsize=(960,540))
        (H,W)=frame.shape[:2]# uzunluk genişlik verileri alınır
        #algoritma güncellenir ve bilgileri çekilir
        (success,boxes)=trackers.update(frame)

        #ekrana bilgilendirme mesajları yazılır
        info=[("Tracker",algorithm),
                ("Success","yes" if success else "no")]
        
        string_text=""
        for (i,(k,v)) in enumerate(info):
            text=f"{k}: {v}"
            string_text=string_text+text
        cv2.putText(frame,string_text,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)    
        #takip algoritmasındaki bilgiler ile tespit edilen cisimler dörtgen içerisinde gösterilir 
        for box in boxes:
            (x,y,w,h)=[int(v) for v  in box ]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow("frame",frame)
        key=cv2.waitKey(1) & 0xFF
        # t ye basılında roi seçilir 
        if key==ord("t"):
            box=cv2.selectROI("frame",frame,fromCenter=False)
            #algoritma başlatıldı
            tracker=OPENCV_OBJECT_TRACKERS[algorithm]()
            # multi tracker eklendi
            trackers.add(tracker,frame,box)
        elif key==ord("q"):break

        f=f+1
cap.release()
cv2.destroyAllWindows()
