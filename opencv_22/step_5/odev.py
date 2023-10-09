import numpy as np 
import cv2

def cember_ciz(event,x,y,flags,param):# çember çizmek için çalışacak olan fonksiyonun parametreleri konunm ve mouse durumu
    global center,clicked # konum ve tıklama durumu fonksiyonda dışında da kullanılabilmesi için globale çevrildi
    # eğer tıklanıyor ise parametreleri sıfırlar ve çemberi göstermez
    # eğer tıklanmıyor ise tıklanmış olan değer ile çember çizer
    if  event==cv2.EVENT_LBUTTONDOWN:
       center=(0,0)
       clicked=False
    elif event==cv2.EVENT_LBUTTONUP:
        center=(x,y)
        clicked=True
      
        
          

cap=cv2.VideoCapture(0)# video yakalandı
cv2.namedWindow("test")# çerçeve isimlendirildi
cv2.setMouseCallback("test",cember_ciz)# tıklama olaylarını çizim için hazırladığımız fonksiyona gönderir

center=(0,0)# merkez kordinatları başlatıldı
clicked=False # tıklama durumu başlatıldı

while True:
    ret,frame=cap.read()# video okundu

    if clicked==True:# tıklama işlemi gerçekleşti ise 
        cv2.circle(frame,center,10,(0,0,255),2)#
    
    cv2.imshow("test",frame)# frameler gösterilir
    
    if cv2.waitKey(1) & 0xFF ==ord("q"): # q ya basınca videoyu durdur
        break
cap.release()
cv2.destroyAllWindows()    




            

            
            







