import imutils
import cv2

image = cv2.imread("pyimagesearch\\lessons\\step3\\test.jpg")#görüntü çekildi


output=image.copy()# üzerinde çizim yapabilmek için resmin bir kopyasını çıktı olarak aldık
cv2.rectangle(output,(320,60),(420,160),(0,0,255),2)# belirlenen konumda kırmızı bir dikdörtgen çizildi
#- burada ilk verdiğimiz ^ konum dikdötgenin  sol üst ikincisi ise sağ alt köşesini belirlemek için yazıldı üçünci paramtrede renk 2 yazan yerde ise kalınlık tanımlandı.
cv2.circle(output,(300, 150), 20, (255, 0, 0), -1)# çember çizerken kullandığımız sondaki -1 parametresi içinin dolu olduğunu belli ediyor
cv2.line(output,(60,20),(400,200),(0,0,255),5)#iki noktası belirlenen çizgi
cv2.putText(output,"output test",(150,200),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
cv2.imshow("rectangle",output)



cv2.waitKey(0)
cv2.destroyAllWindows()