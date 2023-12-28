import cv2
import time
image=cv2.imread("data\\car.jpg")# resim içeri aktarıldı

cv2.imshow("car",image)
cv2.waitKey(0)
cv2.destroyAllWindows()


 
cap=cv2.VideoCapture("data\\video.mp4")# video içeri aktarıldı
width=int(cap.get(3))
height=int(cap.get(4))
print("genislik:",cap.get(3))# 3. index genişlik 
print("yükseklik:",cap.get(4))# 4.index yükseklik verir

if cap.isOpened()==False:# video yüklenmezse buradaki komut çalışır
    print("There is no video")

writer =cv2.VideoWriter('filename.mp4',  
                         cv2.VideoWriter_fourcc(*'mp4v'), 
                         30, (height,width))
  
while True:     # sonsuz döngü haline getirdik sebebi ise cv2 nun videodaki kareleri(frame) tek tek okumasıdır- olan video içinse adresi yazılmalı
    ret,kare=cap.read()# kareleri tak tak okumak için girdik burada girdiğimiz ret fonksiyondan çıkan true false değerini kare ise çıkan kare değerini karşılaması için yazıldı
    if ret == 0:
        break# ret 0 olduğunda video biter ve pencere kapanır
    #kare=cv2.flip(kare,1)# 1 yazarsak her bir kare y eksenine göre tersini alırız ayna etkisi yaratır 
    cv2.imshow("webcam",kare)# anlık videoların karelerini(framlerini)alıcaz  
    writer.write(kare)
    if cv2.waitKey(30)& 0xFF==ord("q"):# her kareyi 30 m/s göreceğiz -q ya basana kadar devam eder
        break
    
cap.release()  
cv2.destroyAllWindows() 

