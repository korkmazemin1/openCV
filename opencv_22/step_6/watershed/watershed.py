import numpy as np 
import cv2
import matplotlib.pyplot as plt

coin=cv2.imread("images\\input\\coin12.jpg")# resim okundu

def display(img,cmap=None):# aldığı resimi gray formatta gösteren fonksiyon
    fig=plt.figure(figsize=(12,10))# resim boyutu belirlenir
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap=cmap)# gray formatta ekrana basıtırılır
    plt.waitforbuttonpress()


display(coin)

coin_gray=cv2.cvtColor(coin,cv2.COLOR_BGR2GRAY)#fotonun renk uzayı graya çevrildi

# fotodaki gürültü oranını azaltmak için median blur uygulanır
blur=cv2.medianBlur(coin,5)# kernel(çekirde) boyutu 25 olarak belirlendi

display(blur)
blur=cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

ret,thresh=cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)# threshold ile istenen pikselleri 1 e eşitleyip altındakileri 0 a eşitleriz# 77 değeri değişken olabilir
thresh=cv2.bitwise_not(thresh)# kurs çıktısı ile benzer gitmek adına siyah beyaz alan değiştirildi

display(thresh,cmap="gray")


contours,hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)#kontur tespiti yapıldı

for i in range(len(contours)):# kontur uzunluğu boyunca for döner
    if hierarchy[0][i][3]==-1:# dış bükey konturları hesaplamak için hierarchy çıktıları koşullanır
        cv2.drawContours(coin,contours,i,(255,0,0),10)# saptanan konturlar çizilir


display(coin)


# görüldüğü üzre konturları bularak yalnızca tüm paraların toplam çevresini tespit edebiliyoruz
# para saptamaya daha mantıklı bir algoritma olan watershed ile devam edicez
                 #################     WATERSHED      #####################

# ilk uygulamadaki blur ile devam ediyoruz 


display(thresh,cmap="gray")


kernel=np.ones((3,3),np.uint8)# gürültüleri gidermek için bir kernel oluşturulur
opening=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=3)# lekeleri kaldırmak adına morfoloji işlemleri uygulanır
# cv2.Morphopen siyah arkaplan içindeki beyaz kirleri kapatır ama eğer morph close kullanırsan beyaz bölge içersindeki siyah lekelerden kurtuluruz

display(thresh,cmap="gray")

sure_bg= cv2.dilate(thresh,kernel,iterations=3)# ön plan görüntüsü

display(sure_bg,cmap="gray")

# ikili sistemdeki beyaz mesafelerin siyah mesafelerine uzaklığını hesaplayan distance transform fonksiyonu çağrılır

dist_transform=cv2.distanceTransform(thresh,cv2.DIST_L2,5)# 5 ile mask boyutunu belirledik

ret,sure_fg=cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)# piksel değerinin en büyük değerinin distance_transformun 0.7 si olması istediğimizi belirttik

display(dist_transform,cmap="gray")
display(sure_fg,cmap="gray")

sure_fg=np.uint8(sure_fg)# fotonun tipini subtract fonksiyonunda kullanmak için değiştirdik
unknown=cv2.subtract(sure_bg,sure_fg)# subtract ile fotoları birleştirdik

display(unknown,cmap="gray")

###### ikili görüntüdeki bağımsız parçaları tespit etmek için connectedComponent      fonksiyonunu kullanıcaz

### subtractda paraların merkezlerini siyah ile belli etmemizin sebebi bu fonksiyon ile bulmaktı

ret,markers=cv2.connectedComponents(sure_fg)
markes=markers+1
markers[unknown==255]=0# 255 olan değerleri belli etmek için 0 a çevirdik

display(markers,cmap="gray")

markers=cv2.watershed(coin,markers)

display(markers)


contours,hierarchy=cv2.findContours(markers.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)


for i in range(len(contours)):
    if hierarchy[0][i][3]==-1:
        cv2.drawContours(coin,contours,i,(255,0,0),10)

display(coin)    


