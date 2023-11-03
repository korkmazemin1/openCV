import numpy as np
import cv2
import time
corner_track_params=dict(maxCorners=10,qualityLevel=0.3,minDistance=7,blockSize=7)

lk_param=dict(winSize=(200,200),# winsize ile takip sisteminin hassasiyetini belirleriz
              maxLevel=2,#level değeri arttıkça çözünürlük değeri düşer
              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))########3
pt1=(0,0)
br=(0,0)
tl=(0,0)
tiklama=False
fx=0
fy=0
lx=0
ly=0

cizim=False
def dortgen_ciz(event,x,y,flag,param):
   global fx,fy,cizim,pt1,lx,ly,tiklama
   
   if tiklama==False:
      if event==cv2.EVENT_LBUTTONDOWN :
      
         fx=x
         fy=y
         tiklama=True
         cizim=True
         
      if  event==cv2.EVENT_LBUTTONUP:
            lx,ly=(x,y)
            cizim=True
      if event==cv2.EVENT_MOUSEMOVE and cv2.EVENT_LBUTTONDOWN:
               cizim=True
               fx=x
               fy=y
   else:
       if event==cv2.EVENT_LBUTTONDOWN :
           tiklama=False
       else:
           tiklama=True    
   

def kontrol(lx,ly):
    if lx!=0 and ly!=0 :
        return True
    else:
        return False      


         
cap=cv2.VideoCapture(0)
cv2.namedWindow("cizim")
cv2.setMouseCallback("cizim",dortgen_ciz)



def roi_creater(lx,ly,fx,fy):# roideki kordinatların değişmesi sebebi ile bu değişiklikleri kontrol eden bir fonksiyon
   
   if fx==fy and lx==ly:
      bigger_x=100
      smaller_x=50
      bigger_y=100
      smaller_y=50
   else:
      Bigger_x=100
      smaller_x=50
      bigger_y=100
      smaller_y=50 
   if ly>fy:
      bigger_y=ly
      smaller_y=fy
   elif fy>ly:
      bigger_y=fy
      smaller_y=ly
   else:
      bigger_x=100
      smaller_x=50
      bigger_y=100
      smaller_y=50   
   if lx>fx:
      bigger_x=lx
      smaller_x=fx
   elif fx>lx:
      bigger_x=fx
      smaller_x=lx
   else:
      bigger_x=100
      smaller_x=50
      bigger_y=100
      smaller_y=50  
   

   return bigger_x,bigger_y,smaller_y,smaller_x
  


while True:
   ret,frame=cap.read()
   if kontrol(lx,ly)==True:
      if cizim==True:
        cv2.rectangle(frame,(fx,fy),(lx,ly),(255,0,0),2)
         
        bigger_x,bigger_y,smaller_y,smaller_x=roi_creater(lx,ly,fx,fy)
        roi=frame[smaller_y:bigger_y,smaller_x:bigger_x]
        cv2.imshow("roi",roi)      
        
         

   cv2.imshow("cizim",frame)



   if cv2.waitKey(30) == 27:
      break
cap.release()   
cv2.destroyAllWindows()



      