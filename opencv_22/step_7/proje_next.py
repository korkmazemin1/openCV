import numpy as np
import cv2
import time
corner_track_params=dict(maxCorners=30,qualityLevel=0.1,minDistance=5,blockSize=7)

lk_param=dict(winSize=(200,200),# winsize ile takip sisteminin hassasiyetini belirleriz
              maxLevel=12,#level değeri arttıkça çözünürlük değeri düşer
              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,0.03))########3
tiklama=True
(fx,fy,lx,ly)=(0,0,0,0)
count=0
again=0
save_roi=None# ilk turda boş dönmemesi için  save_roiye boş bir ekran atadık
same_roi=None
cizim=False
bigger_x,bigger_y,smaller_x,smaller_y=(0,0,0,0)

def dortgen_ciz(event,x,y,flag,param):# ikinci tıklamada dörtgeni kitlesin ve sonraki tıklamada  yeni dörtgene başlasın
   global fx,fy,cizim,pt1,lx,ly,tiklama
   
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
def kontrol(lx,ly):
    if lx!=0 and ly!=0 :
        return True
    else:
        return False      

      
cap=cv2.VideoCapture(0)
cv2.namedWindow("cizim")
cv2.setMouseCallback("cizim",dortgen_ciz)

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
        

        try:
            cv2.imshow("roi",roi)  
        except:
            print("lütfen roi alanını düzgün seçiniz")

        
        same_roi=roi_control2(bigger_x_control,bigger_y_control,smaller_x_control,smaller_y_control,bigger_x,bigger_y,smaller_y,smaller_x)
        
            # buraya roi çekilecek
        if same_roi==True and count==0:# sayac oluştur ve sayac her buraya girmediğinde sıfırlansın böylelikle aynı oldugu zamanlar kaydolan roi değişmez
               
               save_roi=roi # değişmeyen bir roiye sahip olduğumuzda işlem yapılacak alan burası 
               
               count=1 # sayacın koyulmamasının sabebi save_roi nin roiler değişmediği takdirde korunmasını sağlamak 
               #cv2.imshow("save_roi",save_roi)
              
               
        elif same_roi==True and count==1:
               save_roi=save_roi
        else:
            count=0
          
        # bu kısımda kaydedip kitlediğimiz roinin diğer roilerle olan karşılaştırması için gerekli fonksiyonlar yapıldı
        if same_roi:
            if tiklama:
            
                cv2.imshow("save_roi",save_roi)   
            
                 
                prev_frame=save_roi
        
                prev_gray=cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)

                prevPts=cv2.goodFeaturesToTrack(prev_gray,mask=None,**corner_track_params)

                mask = np.zeros_like(prev_frame)
        
                frame_gray =cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                try:
                    nextPts, status, err=cv2.calcOpticalFlowPyrLK(prev_gray,frame_gray,prevPts,None,**lk_param)
                except:
                    print("roi alanını düzgün seçiniz")
                    break
                good_new=nextPts[status==1]
                good_prev=prevPts[status==1]

                for i ,(new,prev) in enumerate(zip(good_new,good_prev)):       

                    x_new,y_new=new.ravel()# ravel ile aynı matris içersindeki iki ayrı diziyi tek boyutlu hale getirip sırası ile yazarız [[1,2,3][4,5,6]] ravelden sonra [1,2,3,4,5,6]
                    x_prev,y_prev=prev.ravel()
                   
                    x_prev=int(x_prev)
                    y_new=int(y_new)
                    y_prev=int(y_prev)
                    x_new=int(x_new)
                    frame=roi
                    mask=cv2.line(mask,(x_prev,y_prev),(x_new,y_new),(0,250,0),3)       
                    
                    frame=cv2.circle(frame,(x_prev,y_prev),8,(0,0,255),-1)
            
                img=cv2.add(frame,mask)                 
                cv2.imshow("frame",img)  

                prev_gray=frame_gray.copy()
                prevPts=good_new.reshape(-1,1,2)             
            else:     
                pass        

   cv2.imshow("cizim",frame)

   if cv2.waitKey(30) == 27:
      break
cap.release()   
cv2.destroyAllWindows()



      