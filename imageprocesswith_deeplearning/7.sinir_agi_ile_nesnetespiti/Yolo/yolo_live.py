import cv2
import numpy as np 
from yolo_model import YOLO

# literatürdeki parametreler ile yolo çekildi
yolo=YOLO(0.6,0.5)

file="data\\coco_classes.txt"

with open(file) as f:
    #sınıf isimler okundu
    class_name=f.readlines()

# sınıflar arasındaki boşluklar kaldırıldı
all_classes=[c.strip() for c in class_name]   

#resim okuma
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    if ret:
        # resim yeniden boyutlandırma
        pimage=cv2.resize(frame,(416,416))
        # dizi ye çevrilme
        pimage=np.array(pimage,dtype="float32")

        # normalizasyon
        pimage/=255.0
        pimage=np.expand_dims(pimage,axis=0)

        #yolo
        boxes,classes,scores=yolo.predict(pimage,frame.shape)


        if classes is not None:

            for box,score,cl in zip(boxes,scores,classes):
                    x,y,w,h=box
                
                    top=max(0,np.floor(x+0.5).astype(int))
                    #x+0.5 ile görsellik için küçük bir pay bırakılmıştır
                    left=max(0,np.floor(y+0.5).astype(int))
                    right=max(0,np.floor(x+w+0.5).astype(int))
                    bottom=max(0,np.floor(y+h+0.5).astype(int))
                    #floor ondalıklı sayıları alta yuvarlayarak integer yapar

                    cv2.rectangle(frame, (top,left),(right,bottom),(255,0,0),2)
                    cv2.putText(frame,f"{all_classes[cl]} {score}",(top,left-6),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,12,250),1,cv2.LINE_AA)
        cv2.imshow("yolo",frame)
        if cv2.waitKey(1)&0XFF==ord('q'):
            break

