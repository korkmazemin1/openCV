from __future__ import print_function
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def order_points_old(pts):
    rect=np.zeros((4,2),dtype="float32")

    s=pts.sum(axis=1)# s değeri kordinatların toplam değerlerini alır
    rect[0]=pts[np.argmin(s)]#sol üst nokta en küçük toplam
    rect[2]=pts[np.argmax(s)]# sağ alt nokta en büyük toplama eşit olur

    diff=np.diff(pts,axis=1)# koşelerin kordinat  farkını diff değişkenine atadık
    rect[1]=pts[np.argmin(diff)]# sağ üst nokta en küçük fark
    rect[3]=pts[np.argmax(diff)]# sol alt nokta en büyük farka denk olur

    return rect

######!!!!!!!!!!!!!!!  ÜSTTEKİ FONKSİYONDA(order_points_old)  YAPILAM İŞLEM SONUCU TOPLAM VEYA FARKLARIN AYNI ÇIKMASI NOKTALARIN SIRALAMASINI YANLIŞ BULMAMIZA SEBEP OLUR
####### BU YÜZDEN HER ZAMAN İŞE YARAYAN BİR YÖNTEM DEĞİLDİR


def order_points(pts):
    xSorted=pts[np.argsort(pts[:,0]),:] # noktaları x kordinatı baz alınarak sıralanır
    # argsort fonksiyonu küçükden büyüğe doğru sıralar
    leftMost = xSorted[:2,:]# x kordinatına göre sırallanmış noktaların içerisinde sol tarafdakileri
    rightMost =xSorted[2:,:]# ve sağ tarafdakileri ayırdık
    
    leftMost =leftMost[np.argsort(leftMost[:,1]),:]# burada ise sol tarafda kalan noktaları y kordinatına göre sıraladık
    (tl,bl)=leftMost# ardından y kordinatına sıralanmış noktalardan  sol üst ve sol alt tanımlandı

    D=dist.cdist(tl(np.newaxis),rightMost,"euclidean")[0]#pisagor teoremine göre  sol üst nokta ile sağdaki noktaların arasındaki öklid mesafesi hesaplandı
    (br,tr)=rightMost[np.argsort(D)[::-1],:]# sol üst nokta ile öklid mesafesi fazla olan nokta sağ alt diğeri ise sağ üst olarak tanımlandı

    return np.array([tl,tr,br,bl],dtype="float32")# saptanan noktalar fonksiyonda döndürüldü



ap = argparse.ArgumentParser()
ap.add_argument("-n", "--new", type=int, default=-1,# default ı -1 girerek parametreyi girme zorunluluğumuzun olmadığını gösteririz
	help="whether or not the new order points  should be used")
args = vars(ap.parse_args())


image=cv2.imread(r"images/object.png")# resim okundu
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
gray=cv2.GaussianBlur(gray(7,7),0)# blur uygulandı
# kenarlar arasındaki boşluğu kapatmak adına erezyon ve dilation kullanılır
edged=cv2.Canny(gray,50,100)
edged=cv2.dilate(edged,None,iterations=1)# dilate ile piksel grupları büyütüldü
edged=cv2.erode(edged,None,iterations=1)# erozyon ve dilate ile ana hatlar arasındaki boşluklar kapandı -erode gürültü engelleyen bir fonksiyondur-


cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)#konturlar bulunur
cnts=imutils.grab_contours(cnts)#konturlar sayısal formata çevriliyor

(cnts,_)=contours.sort_contours(cnts)# konturları soldan sağa sıraladık
colors=((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))# noktaları belli edeceğimiz renklerin bgr değeri girildi

for (i,c) in enumerate(cnts):#enumerate hem elemanı hem indeksini(sıralanmış halinin indeksini) döndürür
    if cv2.contourArea(c)<100:# küçük konturları göz ardı etmek için koşul yazıldı
        continue
    box=cv2.minAreaRect(c)
    box=cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)# nesneyi çevrelemek için kullanılacak dörtgen cv2 kütüphanesinin kontrolü yapılarak bulundu   
    box=np.array(box,dtype="int")# kutunun noktaları için integer tipinde dizi oluşturuldu
    cv2.drawContours(image,[box],-1,(0,255,0),2)# kutu kordinatlarına göre resmin üzerine kutular çizildi

    print(f"Object # {i+1}")# orijinal kordinatlar gösterildi
    print(box)

    rect=order_points_old(box)# noktaları sırasına göre dizmek için daha önceden yazdığımız verimi az olan fonksiyonu çağırdık

    if args["new"]>0:
        rect=perspective.order_points(box)

    print(rect.astype("int"))
    print("")    

    for ((x,y),color)in zip (rect,colors):# köşeleri belirten daireler çizildi
        cv2.circle(image,int(x),int(y),5,color,-1)

    cv2.putText(image,f"Object #{i+1}",(int(rect[0][0]-15),int(rect[0][1]-15)),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,255),2)#nesnelerin numaraların yazılacağı yerler konumları ile beraber verildi ve yazıldı    

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
