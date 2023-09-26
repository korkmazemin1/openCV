"""
optik kağıdının kontrol edebilen mini projenin algoritması

1-resim okundu
2-gray formata çevrildi
3-Gaussian blur yöntemi ile blur uygulandı
4-canny fonksiyonu ile kenarları saptandı
5-konturlar bulundu ve dizi haline geldi
6-kayda değer konturlar if satırı ile kontrol edildikten sonra approxpolydp ile şekil düzeltmeleri uygulandı
7-approx polydp nin kenar çıktısı  ile resim içersinde 4köşesi olan kontur optik kağıt olarak tanımlandı
8-four point transform ile optik kağıt kuş bakışı haline geldi
9-kuş bakışı haline gelen optik kağıda threshold uygulandı
10-ayrıca konturları bulundu
11-daha sonrasında bulunan konturlardan konturların boyutları if satırı ile kontrol edilip şık baloncukları belirlendi
12-baloncuklar yukarıdan aşağıya sıralandı
13-daha sonra baloncuklar soldan sağa sıralanarak şıklar atandı
14-şıkların üzerindeki pixel değerlerine göre işaretlenen şık belirlendi
15-doğru olan şıkların üzeri yeşil çember ile çizildi
16-eğer yanlış işaretleme var ise kırmızı ile çizildi




"""




from  imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,help="path to the input image")
args = vars(ap.parse_args())

ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}# cevap anahtarı 1. soru B 2. soru E

image = cv2.imread(args["image"])# resim yüklendi 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# gri foırmata çevrildi
blurred = cv2.GaussianBlur(gray, (5, 5), 0)# blur uygulandı
edged = cv2.Canny(blurred, 75, 200)# canny ile köşe tespiti yapıldı

cv2.imshow("edged",edged)
cv2.waitKey(0)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)# konturlar bulundu
cnts = imutils.grab_contours(cnts)# konturlar dizi haline getirildi
docCnt = None

if len(cnts) > 0:
    cnts=sorted(cnts,key=cv2.contourArea,reverse=True)

    for c in cnts:
        
        peri=cv2.arcLength(c,True)#konturun uzunluğunu hesaplar
        approx=cv2.approxPolyDP(c,0.04*peri,True)# şekli bozuk olan kontuların şeklini düzeltmek için köşeler listesinde bizim verdiğimiz ikinci
        # parametre ile uzaklığını bizden alıp gereksiz köşeleri görmezden gelir mesela karenin üst kenarının ortasındaki bir köşeyi görmezden gelerek düz bir çizgi çeker

        if len(approx)==4:# bubble sheet yani kodlama kağıdını resimimizdeki tek dörtgen resim olarak alırsak 4 kenarı olan cismimizi buluruz
            docCnt=approx
            break

paper=four_point_transform(image,docCnt.reshape(4,2))
warped=four_point_transform(gray,docCnt.reshape(4,2))#resmi kuşbakışı almayı hem bgr formatta hem de gray formatta yaptık    

cv2.imshow("paper",paper)
cv2.imshow("paper_gray",warped)
cv2.waitKey(0)


thresh=cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]#threshold uygulandı

cv2.imshow("thresh",thresh)
cv2.waitKey(0)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
questionCnts = []

for c in cnts :
    (x,y,w,h)=cv2.boundingRect(c)
    ar=w/float(h)#aspect ratio-- en boy oranı

    if w>=20 and h>=20 and ar>=0.9 and ar<=1.1:# burada  daireleri saptamak için en boy büyüklükleri ve en boy oranı--aspect ratio-- kontrol edilir
        questionCnts.append(c)# karşıladığı takdirdi cevaplar listesine atılır

questionCnts=contours.sort_contours(questionCnts,method="top-to-bottom")[0]#konturları yukarıdan aşağıya sıraladık

correct=0


for(q,i) in enumerate (np.arange(0,len(questionCnts),5)):#arange ilk soruların sıralarını sayarız (0,5,10,15,20)
    cnts=contours.sort_contours(questionCnts[i:i+5])[0]# yukarıdan aşağıya sıraladığımız şıkların aynı satırda olanları sırasıyla her satırı dolanarak soldan sağa sıralıyoruz--sort_counters a metod girmezsek default olarak soldan sağa sıralıyor
    bubbled=None 
    for (j,c) in enumerate (cnts):
        mask=np.zeros(thresh.shape,dtype="uint8")# thresh lediğimiz görsel boyutunda bir alan açtık
        cv2.drawContours(mask,[c],-1,255,-1)# bu boş alana konturları attık

        mask=cv2.bitwise_and(thresh,thresh,mask=mask)
        total = cv2.countNonZero(mask)# en çok sıfır olamayan alana sahip kontur işaretlenmiş olan kontur olduğu için total burda işaretlenmiş şıkka denk gelir

        if bubbled is None or total > bubbled[0]:
            bubbled=(total,j)

    color=(0,0,255)
    k = ANSWER_KEY[q]


    if k == bubbled[1]:# her doğru cevapta doğru sayısı artar tespit rengi yeşil olur
        color =(0,255,0)
        correct +=1


    cv2.drawContours(paper,[cnts[k]],-1,color,3)

score = (correct / 5.0) * 100 
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
print(correct)
cv2.waitKey(0)        



