import cv2
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import time
from cv2 import legacy as lg
"""OPENCV_OBJECT_TRACKERS =  {"csrt":lg.TrackerCSRT.create(),
                              "kcf":lg.TrackerKCF.create(),
                              "boosting":lg.TrackerBoosting.create(),
                              "mil":lg.TrackerMIL.create(),
                              "tld":lg.TrackerTLD.create(),
                              "medianflow":lg.TrackerMedianFlow.create(),
                              "mosse":lg.TrackerMOSSE.create()}# takip algoritmaları sözlük hali ile sıralandı
"""
tracker_name="boosting" # boostingi denemek için değişken içerisine alındı           
                          

gt=pd.read_csv("gt_new.txt")# grand truth bilgileri alındı
frame_no = gt["frame_no"].values
x = gt["x"].values
y = gt["y"].values
w = gt["w"].values
h = gt["h"].values
center_x = gt["center_x"].values
center_y = gt["center_y"].values

print(x[5])


video_path="deneme.mp4"
cap=cv2.VideoCapture(video_path)# video alındı
#genel parametreler
initBB =None#seçilen kutu
fps=25
frame_number = []
success_track_frame_success =0
track_list =[]
start_time =time.time()
f=0
while True:
    time.sleep(1/fps)
    ret, frame = cap.read()

    if ret:
        frame=cv2.resize(frame,dsize=(960,540))
        (H,W)=frame.shape[:2]# uzunluk genişlik verileri alınır

        #gt
        car_gt=gt

        if len (car_gt)!=0:
           
            x_car=x[f]#değerler dizi halinde çekildi
            y_car=y[f]# grand_truth içinden veriler çejilir
            w_car=w[f]
            h_car=h[f]

            center_x_car=center_x[f]
            center_y_car=center_y[f]
            
            cv2.rectangle(frame,(x_car,y_car),(x_car+w_car,y_car+h_car),(0,255,0),2)# kordinatları bilinen nesnenin bounding boxı çizildi
            cv2.circle(frame,(center_x_car,center_y_car),2,(0,0,255),-1)# merkeze bir nokta
        cv2.imshow("frame",frame)
        #key
        key=cv2.waitKey(1)& 0xFF
        if key==ord("t"):
            #selectroi ile belirli bir bölge seçiliyor
            
            initBB=cv2.selectROI("Frame",frame,fromCenter=False)
            bossting=lg.TrackerBoosting.create()
            bossting.init(frame,initBB)# takip algoritması başladı
            
        elif key==ord("q"):break
        frame_number.append(f)
        f =f+1
    else:break
cap.release()
cv2.destroyAllWindows()

                          
      
                          