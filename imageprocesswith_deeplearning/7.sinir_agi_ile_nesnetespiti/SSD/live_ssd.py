import cv2 
import numpy as np 
import os

classes=["background", "aeroplane", "bicycle", "bird", 
         "boat", "bottle", "bus", "car",  "cat", "chair", "cow", "diningtable", 
         "dog", "horse", "motorbike", "person",  "pottedplant", "sheep", "sofa", "train",
         "tvmonitor"]
#her class için renk değerleri verildi
COLORS=np.random.uniform(0,255,(len(classes),3))

network=cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt","MobileNetSSD_deploy.caffemodel")

cap=cv2.VideoCapture(0)      
while True:
    ret,frame=cap.read()

    if ret:
        
    
        (h,w)=frame.shape[:2]
        blob=cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),0.007843,(300,300),127.5)
        
        #parametreler ile tahminler yapıldı
        network.setInput(blob)
        detections=network.forward()
        if detections is not None:
            for j in  np.arange(0,detections.shape[2]):
                # eşik değeri çekilir ve koşullandırılır
                confidence=detections[0,0,j,2]
                if  confidence> 0.3:
                    idx=int(detections[0,0,j,1])
                    box=detections[0,0,j,3:7]*np.array([w,h,w,h])
                    (startX,startY,endX,endY)=box.astype("int")

                    label=f"{classes[idx]}: {confidence}"
                    cv2.rectangle(frame, (startX, startY), (endX, endY),(COLORS[idx]),2)
                    # class ismi için yer tayini
                    y=startY-16 if startY-16 >15  else startY+16

                    cv2.putText(frame,label,(startX ,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,COLORS[idx],2)
    cv2.imshow("ssd",frame)
    if cv2.waitKey(1)&0XFF==ord('q'):
            break  