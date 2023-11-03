import numpy as np 
import cv2
import matplotlib.pyplot as plt


corner_track_params=dict(maxCorners=30,qualityLevel=0.3,minDistance=7,blockSize=7)

lk_param=dict(winSize=(200,200),# winsize ile takip sisteminin hassasiyetini belirleriz
              maxLevel=2,#level değeri arttıkça çözünürlük değeri düşer
              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))########3


cap=cv2.VideoCapture(0)# webcamden görüntü alınır

ret,prev_frame=cap.read()# frameler çekildi

prev_gray=cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)# Kare gray formata çekildi

# video üzerindeki köşeleri belirlemek adına

prevPts=cv2.goodFeaturesToTrack(prev_gray,mask=None,**corner_track_params)# parametre çekerken ** kullanılmasının sebebi parametrenin dict formatında olmasıdır 


mask = np.zeros_like(prev_frame)# bir önceki frami tuttuk# zeros like  çekilen fotonun arrayinin eşleniğinin sıfırını alır

while True:
    ret,frame=cap.read()# frameler okundu
    frame_gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)# frame gray formata çevrilir
    
    nextPts, status, err=cv2.calcOpticalFlowPyrLK(prev_gray,frame_gray,prevPts,None,**lk_param)# status 1 değerini alırsa problem yok demektir

    good_new=nextPts[status==1]
    good_prev=prevPts[status==1]# takip edilecek noktalar belirlendi

    for i ,(new,prev) in enumerate(zip(good_new,good_prev)):# takip edilecek yerler numaralandı
        
        x_new,y_new=new.ravel()# ravel ile aynı matris içersindeki iki ayrı diziyi tek boyutlu hale getirip sırası ile yazarız [[1,2,3][4,5,6]] ravelden sonra [1,2,3,4,5,6]
        x_prev,y_prev=prev.ravel()
        print(x_new,x_prev)
        x_prev=int(x_prev)
        y_new=int(y_new)
        y_prev=int(y_prev)
        x_new=int(x_new)


        mask=cv2.line(mask,(x_new,y_new),(x_prev,y_prev),(0,250,0),3)# tespit edilen köşelerin gittiği yolu çizmek için çizgi

        frame=cv2.circle(frame,(x_new,y_new),8,(0,0,255),-1)# köşeleri gösteren circle

    img=cv2.add(frame,mask)
    cv2.imshow("frame",img)
    cv2.imshow("roi_save",prev_frame)
    k=cv2.waitKey(30) & 0xFF
    if k==27:
            
        break

    prev_gray=frame_gray.copy()
    prevPts=good_new.reshape(-1,1,2)

cap.release()
cv2.destroyAllWindows()

        

        

    




