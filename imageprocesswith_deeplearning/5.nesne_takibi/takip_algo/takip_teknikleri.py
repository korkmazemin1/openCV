import cv2
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import time
import argparse
#import legacy as lg
OPENCV_OBJECT_TRACKERS =  {"csrt":cv2.legacy.TrackerCSRT.create,
                              "kcf":cv2.legacy.TrackerKCF.create,
                              "boosting":cv2.legacy.TrackerBoosting.create,
                              "mil":cv2.legacy.TrackerMIL.create,
                              "tld":cv2.legacy.TrackerTLD.create,
                              "medianflow":cv2.legacy.TrackerMedianFlow.create,
                              "mosse":cv2.legacy.TrackerMOSSE.create}# takip algoritmaları sözlük hali ile sıralandı
print("algoritmalar: \n csrt \n kcf \n boosting \n mil \n tld \n medianflow \n mosse  ")
algorithm=input("lütfen kullanmak istediğiniz algoritmayi seçiniz:")
 



tracker=OPENCV_OBJECT_TRACKERS[algorithm]()# boostingi denemek için değişken içerisine alındı           
                          

gt=pd.read_csv("gt_new.txt")# grand truth bilgileri alındı
frame_no = gt["frame_no"].values
# veriler tek tek çekilir
x = gt["x"].values
print(type(x))
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

        if len (car_gt)!=0 and f<=np.max(frame_no):
           #f=frame_no
            x_car=x[f]#frame sayısına göre takpip konumları çekilir
            y_car=y[f]# grand_truth içinden veriler çejilir
            w_car=w[f]
            h_car=h[f]
            
            center_x_car=center_x[f]
            center_y_car=center_y[f]
            

            cv2.rectangle(frame,(x_car,y_car),(x_car+w_car,y_car+h_car),(0,255,0),2)# kordinatları bilinen nesnenin bounding boxı çizildi
            cv2.circle(frame,(center_x_car,center_y_car),2,(0,0,255),-1)# merkeze bir nokta

        if initBB is not  None:
            # her frame sonu takip algoritmasının güncel değerleri döner
            (succes,box)=tracker.update(frame)
            # grand truthdaki verilerin bittiği yerde takip karesi çizilmemesi için koşul
            if  f<=np.max(frame_no):
                (x_track,y_track,w_track,h_track)=[int(i) for i in box ]# takip konumları gelir

                cv2.rectangle(frame,(x_track,y_track),(x_track+w_track,y_track+h_track),(0,0,255),2)

                success_track_frame_success+=1
                track_center_x=int((x_track+w_track)/2)
                track_center_y=int((y_track+h_track)/2)
                # takip edilen frameler listeye eklenir
                track_list.append([f,track_center_x,track_center_y])# buradaki merkez değerleri ile asıl merkez değerleri karşılaştırılır
            
            # tracker kısmında o an kullanılan algoritma yazar-ileriki süreçte dinamik olarak değiştirilebilir
            info=[("Tracker",algorithm),
                ("Success","yes" if succes else "no")]
            
            # info kısmındaki bilgiler ekrana yansıtılır
            for (i,(o,p)) in enumerate(info):
                text = f"{o}: {p}"
                cv2.putText(frame,text,(10,H -(i*20)-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

        cv2.putText(frame,f"frame no={f}",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)    
        
        cv2.imshow("frame",frame)
        #key
        key=cv2.waitKey(1)& 0xFF
        if key==ord("t"):
            
            print(f)
            #selectroi ile belirli bir bölge seçiliyor
            
            initBB=cv2.selectROI("Frame",frame,fromCenter=False)#köşeden seçmek için false değeri verildi
          
            
            tracker.init(frame,initBB)# takip algoritması başladı
        if key==ord("q"):break
        frame_number.append(f)
        f =f+1
    else:break
cap.release()
cv2.destroyAllWindows()



stop_time=time.time()
time_diff= stop_time-start_time
                          

#algoritma değerlendirme

# takip algoritması için tutulan liste veritabanına dönüştürülür
track_df=pd.DataFrame(track_list,columns=["frame_no","center_x","center_y"])                 

if len(track_df)!=0:
    print("Tracking method",algorithm)
    print("Time",time_diff)
    print("Number of frame to track(gt):",len(gt))
    print("Number of frame to track (track_success)",success_track_frame_success)
    track_df_frame=track_df.frame_no

    gt_center_x=gt.center_x[track_df_frame].values
    gt_center_y=gt.center_y[track_df_frame].values

    track_df_center_x=track_df.center_x.values
    track_df_center_y=track_df.center_y.values

    plt.plot(np.sqrt((gt_center_x-track_df_center_x)**2+(gt_center_y-track_df_center_y)**2))
    plt.xlabel("frame")
    plt.ylabel("öklid mesafesi btw track")
    error=np.sum(np.sqrt((gt_center_x-track_df_center_x)**2+(gt_center_y-track_df_center_y)**2))
    print ("toplam hata:",error)
    plt.show()
    plt.waitforbuttonpress()