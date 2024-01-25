import cv2
import numpy as np 
import matplotlib.pyplot as plt
from os.path import isfile,join
import os 
import pandas as pd 
import seaborn as sns

col_list = ["frame_number","identity_number","left","top","width","height","score","class","visibility"]

data=pd.read_csv("gt.txt",names=col_list)# txt dosyası okundu ve sütun isimleri alındı
# burada class ı gösterebilmek adına dataframe e çevrilir
d_class=pd.DataFrame(data["class"])
plt.figure()
sns.countplot(d_class,x="class")# bu grafik ile veri dağılımına bakarız
plt.waitforbuttonpress()


car=data[data["class"]==3]# arabaların class numarası 3 olduğundan verinin içinde araba olanlar çekil
video_path="deneme.mp4"

cap=cv2.VideoCapture(video_path)

id=29# id numarası 29 olan araç alınacak
numnbeofImage=np.max(data["frame_number"])# pandas hatası verebilir
fps=25
bound_box_list=[]
for i in range(numnbeofImage-1):
    ret,frame=cap.read()
    if ret:
        
        frame = cv2.resize(frame,dsize=(960,540))
        # anlık frame ve id ler and ile eşleşme durumuna alınır
        print(car["frame_number"],car["identity_number"])
        
        filter_id1=np.logical_and(car["frame_number"]==i+1,car["identity_number"]==id)
        

        if len (car[filter_id1])!=0:# aracın kordinat ve boyut bilgileri alınır
            x=int(car[filter_id1].left.values[0]/2)
            y=int(car[filter_id1].top.values[0]/2)
            w=int(car[filter_id1].width.values[0]/2)
            h=int(car[filter_id1].height.values[0]/2)

            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(frame,(int(x+w/2),int(y+h/2)),2,(0,0,255),-1)

            bound_box_list.append([i,x,y,w,h,int(x+w/2),int(y+h/2)])
        cv2.putText(frame,"frame num:"+str(i+1),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255))
        cv2.imshow("frame",frame)
        
        
        if cv2.waitKey(1) & 0xFF ==ord("q"): break
    else: break
cap.release()
cv2.destroyAllWindows()







