from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2


DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}  
# 7 segmentli sayı göstergesinde 1 ler o segmentin açık olduğunu 0 ise kapalı olduğunu belirtir
# 0-9 arası rakamları gösteren bölümleri(segmentleri) tanımladık

image=cv2.imread("images\\input\\sayi.webp")# resim okundu

cv2.imshow("image",image)
cv2.waitKey(0)

# ön işleme
image = imutils.resize(image, height=500)# yeniden boyutlandırıldı
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
blurred = cv2.GaussianBlur(gray, (5, 5), 0)# blur uygulandı

edged = cv2.Canny(gray, 50, 200, 255)# canny ile kenar tespiti yapıldı

cv2.imshow("canny",edged)
cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# kontutlar tespit edildi
cnts = imutils.grab_contours(cnts)# konturlar dizi haline geldi
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)# bulunan konturlar sıralandı
displayCnt = None


for c in cnts:
	
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)# approx poly dp ile bozuk şekiller algotitma ile düzeltilerek şekiller köşe sayısını bulunur ve döndürülür
	
	if len(approx) == 4:# eğer dörtgen tespit edersek onu rakamları tespit edeceğimiz alan olarak belirleriz
		displayCnt = approx
		break
	

warped=four_point_transform(gray,displayCnt.reshape(4,2))# gray formatı kuşbakışı şekline çevirdik
output=four_point_transform(image,displayCnt.reshape(4,2))    # bgr formattaki görseli kuşbakışı şekline çevirdik
cv2.imshow("wrap",warped)



thresh = cv2.threshold(warped, 2, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU )[1]# kuşbakışı lcd görüntüsüne threshold uygulandı
cv2.imshow("thresh",thresh)
cv2.waitKey(0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
thresh=cv2.erode(thresh,kernel,dst=None)
# thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)# morfoloji işlemleri uygulandı

cv2.imshow("close", cv2.resize(thresh,(640,480)))
"""

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# sadece sayıların göründüğü threshold uygulanmış görselde konturlar bulunur
cnts = imutils.grab_contours(cnts)# bu konturlar dizi haline getirilir
digitCnts = []# dizi açıldı

for c in cnts:
	
    (x,y,w,h) = cv2.boundingRect(c)# ayrılan ve threshold uygulanan lcd ekranından tespit edilen konturlara çizilecek karlerin değerleri verildi
	
    if w>=14 and (h>=30 and h<=40):# çizilecek kareler ile tespit edilen konturlar belirli büyüklük şartı ile 
        digitCnts.append(c)# sayılar listesine eklendi
digitCnts=contours.sort_contours(digitCnts,method="left-to-right")[0]# sayıları doğru okumak için soldan sağa sıraladık
digits = []


for c in digitCnts:
    
      
    (x,y,w,h)= cv2.boundingRect(c)# sayıların olduğu konturun etrafını dolanan konturun değerleri atandı
    print(len(cv2.boundingRect(c)))
    roi=thresh[y:y+h,x:x+w]# sayıların olduğu dörtgen alan roi olarak ayrıldı
    roi_s=cv2.resize(roi,(600,600))
    cv2.imshow("roi",roi_s)
    cv2.waitKey(0)
    (roiH,roiW)=roi.shape
    (dW,dH)= (int(roiW*0.25),int(roiH*0.15))# burada roi nin alan oranları ile 
    dHC=int(roiH* 0.05)# her bir segmentin  yalaşık konumları hesaplanır 

    segments = [
		((0, 0), (w, dH)),	# üst
		((0, 0), (dW, h // 2)),	# sol-üst
		((w - dW, 0), (w, h // 2)),	# sağ -üst
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # merkez
		((0, h // 2), (dW, h)),	# sol -orta
		((w - dW, h // 2), (w, h)),	# sağ-orta
		((0, h - dH), (w, h))	# orta--- her bir  segmentin konumları  belirlendi
	]
    on = [0] * len(segments)
    
    for (i,((xA,yA),(xB,yB))) in enumerate(segments):
          
          segROI=roi[yA:yB,xA:xB]
          #cv2.imshow("segroi",segROI)
          #cv2.waitKey(0)
          #cv2.imshow("roi",roi)
          #cv2.waitKey(0)
          total=cv2.countNonZero(segROI)# konumlarına göre baktığımız segmentlerin üstündeki piksellerin sıfır olanlarına bakılır
          area=(xB - xA) * (yB - yA)# konumuna göre segmentin alanı

          if total / float(area) > 0.5:
               on[i]= 1  # alanına göre segmentin üzerinde yüzde elliden fazla doluluk oranı var ise o segmenti dolu kabul ederiz

    digit = DIGITS_LOOKUP[tuple(on)]# bulduğumuz segmentlere tanımlı segmentler arasından bakılır
    digits.append(digit)
    cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 1)# sayıyı saran dörtgen çizilir
    cv2.putText(output, str(digit), (x - 10, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)  #saptanan sayı yazılır        


print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Input", image)
output=cv2.resize(output,(600,600))
cv2.imshow("Output", output)
"""

cv2.waitKey(0)
cv2.destroyAllWindows()