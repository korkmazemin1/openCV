"""
şekilleri sağdan-sola,aşağıdan- yukarıya sıralayan mini projenin algoritması 

bu projede iki temel fonksiyon var

1-sort_contours:
cnts parametresi saptanan kontuları, method ise sıralama şeklini isteyen parametredi
1-eğer sağdan sola veya aşağıdan yukarıya ise tersten sıralama aktif
2-eğer alt yukarıdan aşağıya veya aşağıdan yukarıya sıralanaksa i=1-- bu atama ilerki satırlarda sıralamanın y ekseni üzerinde olmasını sağlayacak--
3-konturların etrafını saran en küçük dörtgeni belirle
4-istenen değerlere göre konturları sırala-- kod yazımını öğrenmek isteyenler için mutlak anlaşılması gereken bir satırdır bkz:
5-srıalanmış kontur ve çevreleyen dörtgen dizisini sonuç olarak döndür

2-draw_contours:
bu fonksiyon konturların merkezini bulup sırasını merkezin üstüne yazmamızı sağlar

ana algoritma
1-resmi oku
2- kenar tespiti için boş bir sayfa aç
3-resmi split ile kanalların ayırıp her birini ayrı döndüren bir for döngüsü aç
4-kanallara için ayrı ayrı blur uygula
5- kenar tespiti yap
6- konturları bul ve dizi haline getir
7-sort_contours fonksiyonunu çağır ve sonuçları göster

"""





from datetime import datetime
import numpy as np
import argparse
import imutils
import cv2

def sort_contours(cnts,method="left-to-right"):
    reverse=False
    i = 0

    if method=="right-to-left" or method=="bottom-to-top":
        reverse=True
        # burada sağdan sola ve alttan üstte sıralama yapılırken kordinatlar azaldığı için tersten sıralama reverse=True değerine  geldi
    if method=="bottom-to-top" or method=="top-to-bottom":# kordinatlar artan kısımda olduğu için reverse false olarak kalmaya devam eder
        i=1 # bu koşulda sıralamalar y ekseninde olduğu için bunu i=1 ile belirtiriz

    boundingBoxes=[cv2.boundingRect(c) for c in cnts]# tek satırılık for döngüsü ile konturların etrafını saran kutular değişkene atandı
    (cnts,boundingBoxes)=zip(*sorted(zip(cnts,boundingBoxes),key=lambda b:b[1][i],reverse=reverse))# konturları ve sınırlayıcı kutuları beraber sıraladık
    #ikinci zip fonksiyonunun içersinde key=lambda b:b[1][i] parametresindeki [1] bizim vermiş olduğumuz ilk parametredeki
    #boundingBoxesi temsil eder i sayısı ise ana fonksiyonumuzdaki parametreye göre i yi 0 veya bir yani x veya y  kordinatlarını temsil eder
    #x=0,y=1 sıralama yapılacak eksen belirlenir



    return (cnts,boundingBoxes)

def draw_contour(image,c,i):
    M=cv2.moments(c)
    cX=int(M["m10"]/ (M["m00"]+ 1e-7))
    cY=int(M["m01"]/(M["m00"]+ 1e-7))#moments ile beraber şekillerin merkezini bulduk

    cv2.putText(image,f"<{i+1}>",(cX-20,cY),cv2.FONT_HERSHEY_COMPLEX,1.0,(255,255,255),2)# sıralama sonuçlarını şekillerin üstüne yazdırdık

    return image

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the input image")
ap.add_argument("-m", "--method", required=True, help="Sorting method")
args = vars(ap.parse_args())

image=cv2.imread(args["image"])# resim okundu
accumEdged=np.zeros(image.shape[:2],dtype="uint8")#edgemap için hafızadan alan açıldı

for chan in cv2.split(image):# resimi split ile kanallarına-BGR- ayırarak döngü içersinde her biri ayrı ayrı işleme alınacak
    chan=cv2.medianBlur(chan,71)# ayrışmış olan kanallara blur uygulandı
    edged=cv2.Canny(chan,50,200)# canny ile kanala kenar tespiti uygulandı
    accumEdged=cv2.bitwise_or(accumEdged,edged)# numpy ile kenarlar için oluşturuğumuz boş sayfaya tespit edilen kenarlar sırası ile eklenir
    cv2.imshow("EDGE MAP",accumEdged)
    cv2.waitKey(0)
    # bitwise_or ile eğer aynı ka
cv2.imshow("EDGE MAP",accumEdged)


cnts=cv2.findContours(accumEdged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar tespit edildi
cnts=imutils.grab_contours(cnts)# konturlar dizi haline getirildi
cnts=sorted(cnts,key=cv2.contourArea,reverse=True)# reverse parametresine true değeri girildiğinden sorted fonksiyonu sıralamayı tersten yapar
orig=image.copy()

for (i,c) in enumerate(cnts):
    orig=draw_contour(orig,c,i)#konturlar ve enumerate ile onlara atanan sıra sayısı fonksiyona parametre olarak atanır


cv2.imshow("unsorted",orig)
(cnts,boundingBoxes)=sort_contours(cnts,method=args["method"])#sıralanması için kontur fonksiyona atandı

for (i,c) in enumerate(cnts):
    draw_contour(image,c,i)


now=datetime.now()
now=now.strftime('%Y_%m_%d_%H_%S')
cv2.imwrite(f"images/output/output_{now}.jpg",image)
cv2.imshow("sorted",image)
cv2.waitKey(0)    



