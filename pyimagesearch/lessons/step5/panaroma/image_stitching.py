from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,help="path to the output image")
ap.add_argument("-c", "--crop", type=int, default=0,help="whether to crop out largest rectangular region")
args = vars(ap.parse_args())

print("[BİLGİLENDİRME] Resim Yükleniyor..")
imagePaths = sorted(list(paths.list_images(args["images"])))# resimler liste sıralandı
images=[]

for imagePath in imagePaths:
    image =cv2.imread(imagePath)
    images.append(image)


print("[BİLGİLENDİRME] Resimler birleştiriliyor") 
stitcher = cv2.createStitcher() if imutils.is_cv3() else  cv2.Stitcher_create()
(status,stitched) =stitcher.stitch(images)

if status==0:# sıfır ise başarılı
    if args["crop"] > 0:
        print("[BİLGİLENDİRME] Croplama işlemi yapılıyor")
        stitched = cv2.copyMakeBorder(stitched,10,10,10,10,cv2.BORDER_CONSTANT,(0,0,0))

        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)# gray formata çevir
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1] # threshold uygulayıp arkaplanı ortaya çıkardık


        # bundan sonra yapacaklarımız kontur hesaplaması ile arkaplandaki en büyük dörtgeni bulup keseceğimiz görüntüyü yalnızca oraya eklemek
        cnts = cv2. findContours ( thresh.copy () , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE )# arkaplan konturları bulundu
        cnts = imutils. grab_contours ( cnts )# dizi haline geldi
        c = max(cnts,key=cv2.contourArea)# saptanan konturlardan en büyüğü alındı
 

        mask = np.zeros(thresh.shape,dtype="uint8")# resmi kırpılmış hali ile eklemek için alan açıldı
        (x,y,w,h)=cv2.boundingRect(c)# en büyük konturu gösteren dörtgenin verileri girildi
        cv2.rectangle(mask,(x,y),(x+w,y+h),255,-1)# dörtgen çizildi


        minRect = mask.copy()
        sub =mask.copy()

        while cv2.countNonZero(sub) > 0: # arka plan görüntüsü 0 olana kadar devam eder
            minRect =cv2.erode(minRect,None) # ön plandaki nesnenin sınırları aşındırılır
            sub = cv2.subtract(minRect,thresh)# farklı noktalara yerine beyaz piksel  ataması yapılarak iki görsel arasındaki farkı  ortaya çıkarır 

        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
            
        (x, y, w, h) = cv2.boundingRect(c)
           
        stitched = stitched[y:y + h, x:x + w]
        # burada öncelikle arka siyah kenarlıklardan arındırdıktan sonraki alanı tanımlamak için çizdiğimiz dörtgeni tespit edip eski resimden o kare boyutunda olan alanı çektik    
            
        cv2.imwrite("images\\output\\{}".format(args["output"]),stitched)
        cv2.imshow("Stitched", stitched)
        cv2.waitKey(0)
    else:
        print(f"[BİLGİLENDİRME] Resim ekleme iptal edildi ({status})")        