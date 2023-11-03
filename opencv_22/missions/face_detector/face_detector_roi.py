import numpy as np
import cv2
tiklama=True
(fx,fy,lx,ly)=(0,0,0,0)
count=0
cizim=False
bigger_x,bigger_y,smaller_x,smaller_y=(0,0,0,0)
def dortgen_ciz(event,x,y,flag,param):# ikinci tıklamada dörtgeni kitlesin ve sonraki tıklamada  yeni dörtgene başlasın
   
   global fx,fy,cizim,lx,ly,tiklama
   
   if tiklama==False:
      if event==cv2.EVENT_LBUTTONDOWN :
      
        fx=x
        fy=y
        tiklama=True
        cizim=True
        
      elif  event==cv2.EVENT_LBUTTONUP:
            lx,ly=(x,y)
            cizim=True
      elif event==cv2.EVENT_MOUSEMOVE and cv2.EVENT_LBUTTONDOWN:
            cizim=True
            fx=x
            fy=y
   else:
      if event==cv2.EVENT_LBUTTONDOWN :
           tiklama=False
      else:
           tiklama=True    
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def kontrol(lx,ly):
    if lx!=0 and ly!=0 :
        return True
    else:
        return False      

def roi_creater(lx,ly,fx,fy):# roideki kordinatların değişmesi sebebi ile bu değişiklikleri kontrol eden bir fonksiyon
   
    global bigger_x,bigger_y,smaller_y,smaller_x
    
    if fx==fy and lx==ly:
       print("lütfen dörtgeni düzgün ciziniz")
    
    if ly>fy:
       bigger_y=ly
       smaller_y=fy
    elif fy>ly:
       bigger_y=fy
       smaller_y=ly
      
    if lx>fx:
       bigger_x=lx
       smaller_x=fx
    elif fx>lx:
       bigger_x=fx
       smaller_x=lx
    

def roi_control(bigger_x,bigger_y,smaller_y,smaller_x):
    global bigger_x_control,bigger_y_control,smaller_x_control,smaller_y_control
    bigger_x_control=bigger_x
    smaller_x_control=smaller_x
    bigger_y_control=bigger_y
    smaller_y_control=smaller_y 
def roi_control2(bigger_x_control,bigger_y_control,smaller_x_control,smaller_y_control,bigger_x,bigger_y,smaller_y,smaller_x):
    if bigger_x==bigger_x_control and bigger_y_control==bigger_y and smaller_x==smaller_x_control and smaller_y==smaller_y_control:
        same_roi=True
    else :
        same_roi=False     
    return same_roi  
cap=cv2.VideoCapture(0)
cv2.namedWindow("face")
cv2.setMouseCallback("face",dortgen_ciz)
while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
   
    if kontrol(lx,ly)==True:
      
      if cizim==True:
            cv2.rectangle(frame,(fx,fy),(lx,ly),(255,0,0),2)
        
            roi_control(bigger_x,bigger_y,smaller_y,smaller_x)

            roi_creater(lx,ly,fx,fy)
            
        
            #while geçtikten sonra kordinat kontrolü 
        
            roi=frame[smaller_y:bigger_y,smaller_x:bigger_x]
        

        
            
            face_recs=face_cascade.detectMultiScale(roi)# cascade ile tespit yapıldı

            for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
                cv2.rectangle(roi,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi
        
            cv2.imshow("roi",roi)
        

    

    
    if cv2.waitKey(30) == 27:
      break
    cv2.imshow("face",frame)
cap.release()   
cv2.destroyAllWindows()


