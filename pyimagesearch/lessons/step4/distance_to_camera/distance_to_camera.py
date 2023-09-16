"""
KAMERA İLE UZAKLIK HESAPLAMA

Bu mini projede kağıdı işaretçi olarak kullandığımız bir mesafeyi nasıl hesapladığımızı göreceksiniz
find_marker

1-resim gray formata çevrilir
2-blur uygulanır
3-canny fonksiyonu ile kenarlar saptanır
4-konturlar saptanır(en büyük kontur kağıt olarak kabul edildi)
5-kağıdın etrafını saran en küçük dörtgen belirlenir
distance to camera fonksiyonunda ise hesap kısmı var


1-resim yolu ve gerekli değerler input olarak alınır
2-resim yüklenir
3-findmarker(resim) çağrılır
4-uzaklık hesaplanır

birden fazla resimde hesap için

1-resimler tek tek dönen bir for döngüsü açılır
2-resim okunur
3-findmarker ile kağıt satanır
4-uzaklık hesabı yapılır
5-kutu çizilir ve uzaklık resme yazılır

"""



from imutils import paths
import numpy as np
import imutils
import cv2



def find_marker(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)#resim gray formata çevrildi
    gray=cv2.GaussianBlur(gray,(5,5),0)# resime blur uygulandı
    edged=cv2.Canny(gray,35,125) # canny ile kenar tespiti yapıldı

    cnts=cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)# kontürler saptandı
    cnts=imutils.grab_contours(cnts)#saptanan kontürler toplandı
    c=max(cnts,key=cv2.contourArea)# kontürler arasından en büyük olanı kağıt parçamız olarak kabul ediyoruz

    return cv2.minAreaRect(c)# kağıdın etrafını saran en küçük dörtgen fonksiyonda döner
def distance_to_camera(knownWidth,focalLenth,perWidth):
    return(knownWidth*focalLenth/perWidth)# bu fonksiyon uzaklığı hesaplamak için gereken işlemleri yapa

                ###bu kısımda referans noktası aldığımız kağıdın uzaklığını ve genişliğini statik olarak aldık  
#KNOWN_DISTANCE = 24.0
#KNOWN_WIDTH = 11.0

#kullanışsız olan bu yöntemi dinamik olarak alarak daha faydalı bir kod yapısı elde edelim
KNOWN_DISTANCE =int(input("isaretleyici olarak kullanilan kagidin kameraya olan uzakligini giriniz:"))
KNOWN_WIDTH =int(input("isaretleyici olarak kullanilan kagidin genisligini  giriniz:"))
resim=input("klasöre attiginiz görselin ismini uzantisi ile giriniz")
image = cv2.imread(resim)# resim okunur
marker = find_marker(image)# kağıt saptanır
focalLength = (marker[1][0] * KNOWN_DISTANCE) /KNOWN_WIDTH# uzaklık hesabı yapılır

for imagePath in sorted(paths.list_images("images")):# döngü ile beraber listeden resimler alınır
    image=cv2.imread(imagePath)# resimler okunur
    marker=find_marker(image)# eldeki resimdeki kağıt saptanır
    inches=distance_to_camera(KNOWN_WIDTH,focalLength,marker[1][0])# ardından kamera ile mesafesi hesaplanır

    box=cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)# cv2.sürüm kontrolü ile beraber saptanan kağıda kutu çizilir
    box=np.int0(box)
    cv2.drawCounters(image,[box],-1,(0,255,0),2)# konturlar çizilir
    cv2.putText(image, "%.2fft"% (inches / 12),(image.shape[1]-200,image.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,2.0,(0,255,0),3)# hesaplanan uzaklık resmin üstüne yazılır
    
cv2.imshow("image",image)
cv2.waitKey(0)
cv2.destroyAllWindows()


