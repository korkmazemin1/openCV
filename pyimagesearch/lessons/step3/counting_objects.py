import cv2
import imutils
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
args = vars(ap.parse_args())
#^^^^komut satırı için gereken kodlar^^^^^^^
#####                                          ##### 
#####BU KODDA RESİM OLARAK test3.jpg KULLANILDI#####
#####                                          #####
image=cv2.imread(args["image"])
cv2.imshow("image",image)

#resim okundu
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# resim gray formata çevrildi

cv2.imshow("gray",gray)
edged=cv2.Canny(gray,30,150)# canny fonksiyonundaki paramtreler sırası ile minimum ve maksimum thresholdu tanımlar yapacağın işe göre optimize edebilirsin
#resimin kenarları saptandı
cv2.imshow("kenar",edged)

thresh=cv2.threshold(gray,225,255,cv2.THRESH_BINARY_INV)[1]#threshold fonksiyonu siyah beyaz(gray) formdaki resmin 225 den sonra 255-opsiyonel- e kadar olan renk değerlerini renk olarak yoğun saptayıp çıktı olarak bu kısımları beyaz gösterir kalan alanları ise siyah verir
cv2.imshow("threshold",thresh)

cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# threshlenmiş görüntüdeki kenarlar saptandı
cnts=imutils.grab_contours(cnts)# saptanan değerler düzenlendi
output=image.copy()

for c in cnts:
    cv2.drawContours(output,[c],-1,(240,0,255),3)# saptanan kenarlar döngü içerisinde çizildi
    cv2.imshow("counters",output)

text=f"{len(cnts)} adet nesne saptadim"
cv2.putText(output,text,(10,25),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(240,0,209),2) # nesne sayısı alınarak metin eklendi

cv2.imshow("counter",output)


mask=thresh.copy()
mask=cv2.erode(mask,None,iterations=5)# erpde işlemi threshlenmiş görüntüdeki gürültüleri-minik çıkıntıları- gidererek daha temiz bir görsel almamızı sağlıyor
cv2.imshow("eroded",mask)


mask=thresh.copy()
mask=cv2.dilate(mask,None,iterations=5)# burada kenarları biraz daha geniş alana yayarak cisimler arasında bağlantı kurma sağlanabilir test3 görselinde değerler ile oyanır ise sağlanır
cv2.imshow("dilated",mask)

mask=thresh.copy()
output=cv2.bitwise_and(image,image,mask=mask)# threshold kısmında belirttiğimiz renk değerlerinin altında kalan yani maskelenmiş bölgeleri resimin orijinal halinde tamamen kapattık ve gördüğün üzere test3 resminde bloklar dışında kalan alan siyahtır
cv2.imshow("bitwise",output)



cv2.waitKey(0)
cv2.destroyAllWindows()
