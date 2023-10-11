import numpy as np 
import cv2
import matplotlib.pyplot as plt

kelogs=cv2.imread("images\\input\\kelogs.webp",0)# resim gray formatta okundu
kelogs_raf=cv2.imread("images\\input\\kelogs_raf.jpg",0)# resimler okundu

def display(img,cmap="gray"):# aldığı resimi gray formatta gösteren fonksiyon
    fig=plt.figure(figsize=(12,10))# resim boyutu belirlenir
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")# gray formatta ekrana basıtırılır
    plt.waitforbuttonpress()

display(kelogs)  
display(kelogs_raf)# fotoları fonksiyonu çağırarak ekrana bastırdık

# kelogsu rafdan tespit edecek 3 adet metod denenecek


### BRUTE FORCE DETECTİON with ORB Description#### 1. metod

orb=cv2.ORB_create() # orb detektörü başlatıldı

kp1 , dest1,=orb.detectAndCompute(kelogs,None)# fonksiyonun çıktıları keypoint ve descriptors(tanımlayıcı)
kp2 , dest2=orb.detectAndCompute(kelogs,None)# burada None parametresi ile mask uygulamak istemediğimizi belirttik

bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)#BF Matcher fonksiyonu  aldığı features(özellikler) i aralarındaki uzaklıklara bakarak bağlantı kurar

matches= bf.match(dest1,dest2)#iki kısımında tanımlayıcılar arasında eşleşmeleri buluruz

matches=sorted(matches,key=lambda x:x.distance) # eşleşmeleri yakınlıklarına göre sıraladık # burada sıralamanın kategorisini key ile belirttiğimiz parametre belirler

cizdirme =cv2.drawMatches(kelogs,kp1,kelogs_raf,kp2,matches[:25],None,flags=2)# # matches parametresi ile  0 dan 25 e kadar olan eşleşmeleri göstermek istediğimizi belirttik# None ile mask kullanmak istemediğimizi 
#flags=2 default girildi ve fotolarla beraber keypointleride verildi

display(cizdirme)

### Brute Force Matching ile SIFT Descriptors ve Radio test### 2. metod # ilk metoda göre daha iyi 


sift=cv2.SIFT_create()# fonksiyonumuzu  başlattık

kp1, dist1 = sift.detectAndCompute(kelogs,None)# keypointleri ve tanımlayıcıları iki foto içinde aldık
kp2, dist2 = sift.detectAndCompute(kelogs_raf,None)# None parametresi mask kullanmamak için yapıldı

bf = cv2.BFMatcher()
matches=bf.knnMatch(dist1,dist2,k=2)# k=2 değeri ile en iyi ilk 2 matchi seçmek istediğimizi belirttik

good=[]

for match1,match2 in matches: # eşleşmeleri 1 ve 2. si olarak döndürürüz
    if match1.distance <0.75*match2.distance: # match 2 nin mesafesinin yüzde 75 i 1 inkinden büyükse
        good.append([match1])# birinciyi iyi eşleşme listesine atarız


cizdirme2=cv2.drawMatchesKnn(kelogs,kp1,kelogs_raf,kp2,good,None,flags=2)# None  ile mask kullanmak istemediğimizi flags=2 ise default

display(cizdirme2)# ekran çıktılarında daha sağlam eşleşme elde ettiğimiz görülür

### FLANN based Matcher ### 

sift=cv2.SIFT_create()# sift algoritmasını çalıştıran algoritmayı başlattık

kp1, dest1 = sift.detectAndCompute(kelogs,None)# keypointleri ve tanımlayıcıları iki foto içinde aldık
kp2, dest2 = sift.detectAndCompute(kelogs_raf,None)# None parametresi mask kullanmamak için yapıldı

# >>flann based match fonksiyonu için gerekli default değerler

FLANN_INDEX_KDTREE=0
index_params=dict(algorithm= FLANN_INDEX_KDTREE,trees = 5)
search_params = dict(checks=50)

#>>

flann=cv2.FlannBasedMatcher(index_params,search_params)# flann algoritmasına parametreler girilir

matches= flann.knnMatch(dest1,dest2,k=2)#eşleşmeleri knn match ile değişkene atarız

good = []

for i,(match1,match2) in enumerate(matches):# eşleşmeleri numaralandırarak for ile döndürüyoruz
    if match1.distance < match2.distance*0.7:# ikini eşleşmenin yüzde 70 i biri geçiyorsa 
        good.append([match1])# birinci eşleşme iyi eşleşmeler listesine alınır(good)

cizdirme3= cv2.drawMatchesKnn(kelogs,kp1,kelogs_raf,kp2,good,None,flags=0)#saptadığımız eşleşmeler ve default parametreler ile çizim fonksiyonumuzu çalıştırdık
display(cizdirme3)        


matchesMask=[[0,0]for  i in range(len(matches))]# mask  için değerler girildi

for i,(match1,match2) in enumerate(matches):# eşleşmeleri numaralandırarak for ile döndürüyoruz
    if match1.distance <  0.7*match2.distance:# ikini eşleşmenin yüzde 70 i biri geçiyorsa 
        matchesMask[i]=[1,0] # masklara göre 

draw_params=dict(matchColor =(0,255,0),singlePointColor=(255,0,0),matchesMask=matchesMask,flags=0)# tespit görüntülemelerine daha iyi bir çıktı için renkleri kendimiz ayarladık

cizdirme4=cv2.drawMatchesKnn(kelogs,kp1,kelogs_raf,kp2,matches,None,**draw_params)# tespit sonuçları çizildi

display(cizdirme4)




