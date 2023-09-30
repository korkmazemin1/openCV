import argparse
import imutils
import cv2

#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the video file")
#args = vars(ap.parse_args())


camera=cv2.VideoCapture(0)# video çekildi


while True :
    (grabbed,frame)=camera.read()# kareler okundu
    status="No targets"
    


    if not grabbed:# grabbed değeri bir bool dur ve eğer video bittiyse Bize false değeri verir bunun sonucunda bizde işlemi durdururuz
        break


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#kare gray formata çevrildi
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)# kareye blur uygulandı
    edged = cv2.Canny(blurred, 50, 150)#kareye kenar tespiti yapıldı

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu 
    cnts = imutils.grab_contours(cnts)# bulunan konturlar dizi haline getirildi

    for c in cnts:
         
        peri=cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.01*peri,True)# approxpolydp şekli bozuk olan çokgensel şekilleri bizim belirlediğimiz oranda düzeltir

        if len(approx) >= 4 and len(approx) <= 6:# konturun yaklaşık bir kare olup olmadığına bakılır
            (x, y, w, h)= cv2.boundingRect(approx)# tespit edilen karenin etrafını saran en küçük dörtgenin boyutları alınır
            aspectRatio= w / float(h)# en boy oranı hesaplanır

            area=cv2.contourArea(c)
            hullArea=cv2.contourArea(cv2.convexHull(c))
            solidity=area/float(hullArea)# normal alan ve dış bükey alanı hesaplanarak alanın sağlamlığına bakılır

            keepDims = w > 25 and h>25 # uzunluk genişlik sınırı
            keepSolidity = solidity>0.4# sağlamlık sınırı
            # dipnot: kodu test ederken keepsolidity çıkarıp ayrıca denendi ve doğruluk kontrolünün saçma sonuçların önüne geçtiği anlaşır
            keepAspectRatio = aspectRatio >= 0.3 and aspectRatio <= 3 # en boy oranı sınırları


            if keepDims and keepAspectRatio and keepSolidity:# kontrol değerleri True verir yani sağlar ise 
                cv2.drawContours(frame, [approx], -1, (0, 0, 255), 4)
                status = "Target(s) Acquired"

                M= cv2.moments(approx)
                cX=int(M["m10"]/ (M["m00"]+ 1e-7))
                cY=int(M["m01"]/(M["m00"]+ 1e-7))# tespit edilen karenin orta nokta kordinatları hesaplandı

                (startX, endX) = (int(cX - (w * 0.15)), int(cX + (w * 0.15)))# çizelecek artının x ekseninde başlangıç ve bitiş noktaları
                (startY, endY) = (int(cY - (h * 0.15)), int(cY + (h * 0.15)))# çizelecek artının y ekseninde başlangıç ve bitiş noktaları

               
                cv2.line(frame, (startX, cY), (endX, cY), (0, 0, 255), 3)
                cv2.line(frame, (cX, startY), (cX, endY), (0, 0, 255), 3)# artı çizimi için düz çizgiler

   
    cv2.putText(frame, status, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 255), 2)# ekrana hedefin tespit edilip edilmediğini yaz
	

    cv2.imshow("edged", edged)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
	
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()            