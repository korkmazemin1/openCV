import cv2
import numpy as np
# ilk while da statik bir dörtgen çizim işlemi var
# ikinci while döngüsünde ise mouse ın tıklama hareketine göre dörtgen çizilmiştir
cap=cv2.VideoCapture(0)# webcamdeki görüntüler çekildi

width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)# videonun genişliğini çektik
height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)# videonun uzunluğu çekildi

while True:
    ret,frame=cap.read()# frameler okunuyor
    # ret bize framein okunup okunmadığını belirtir

    x= int(width //2) # enin yarısı boyutunda integer değer
    y= int(height//2) # yüksekliğin yarısı boyutunda integer değer
    #(x,y) sol üst noktamız

    w=int(width//4)
    h=int(height//4) # sağ alt köşe noktaları belirlendi
    
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)# kordinatları hesaplanan kareyi çizdik
    
    cv2.imshow("rectangle",frame)# frameler gösterilir
    
    if cv2.waitKey(1) & 0xFF ==ord("q"):# q ya bastığında çık
        break

cap.release()
cv2.destroyAllWindows()    

def dikdortgen_ciz(event,x,y,flag,param): # bu fonksiyon ile mouse hareketlerine göre dikdötgen çizdirilir
    
    global pt1,pt2,topLeft_clicked,botRight_clicked

    if event==cv2.EVENT_LBUTTONDOWN:# mouse da sol taraf tıklandı ise 
         # aşağıdaki koşullarda tıkalamalara sırasıyla
         # 2 kere tıklanmışsa öncesinde değerleri sıfırla tıklanmadı ise pas geç
         # eğer ilk tıklamada ise sol üst noktanın kordinatlarını al ve True değerini ver
         # eğer  ikinci tıklamada ise sağ üstü  noktanın kordinatlarınnı al ve True değerini döndür
        if topLeft_clicked==True & botRight_clicked==True: # eğer iki tıklamada gerçekleşti ise noktalar ve durumlar sıfırlanır
            pt1=(0,0)# tıklama ile belirlenecek ilk nokta--sol üst
            pt2=(0,0)# ikini sağ alt
            # 2 tıklamadan sonra olduğu için iki boolda sıfırlanır
            topLeft_clicked=False
            botRight_clicked=False
        
        if topLeft_clicked==False:# ilk tıklama
            pt1=(x,y)# sağ üst köşenin kordinatları
            topLeft_clicked=True

        elif botRight_clicked==False:# ikinci tıklama
            pt2=(x,y)# sağ alt köşenin kordinatları
            botRight_clicked=True



pt1=(0,0)# tıklama ile belirlenecek ilk nokta--sol üst
pt2=(0,0)# ikini sağ alt

topLeft_clicked=False
botRight_clicked=False

cap=cv2.VideoCapture(0)# video yakalandı
cv2.namedWindow("test")# çerçeve isimlendirildi
cv2.setMouseCallback("test",dikdortgen_ciz)# tıklama olaylarını çizim için hazırladığımız fonksiyona gönderir

while True:
    ret,frame=cap.read()# frame okundu
    if topLeft_clicked==True : # eğer sol üst işaretlendi ise 
        cv2.circle(frame,center=pt1,radius=5,color=(0,0,255),thickness=-1)# içi dolu küçük bir çember sol tık yapılan konuma çizildi
    if topLeft_clicked and     botRight_clicked:
        cv2.rectangle(frame,pt1,pt2,(0,0,255),2)  # tıklanılan noktaları kullanarak dörtgen çizildi

    cv2.imshow("test",frame)# frameler gösterilir
    
    if cv2.waitKey(1) & 0xFF ==ord("q"): # q ya basınca videoyu durdur
        break
cap.release()
cv2.destroyAllWindows()    