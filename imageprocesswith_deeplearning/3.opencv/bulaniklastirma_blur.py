import cv2
import numpy as np
from imshow import plt_imshow
image=cv2.imread("data\\manzara_constrat.jpg")
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)#plt için rgb ye çevrildi

plt_imshow(image)

dst=cv2.blur(image,ksize=(5,5))# çıktılar dökümantasyona dst olarak isimlendiriliyor
plt_imshow(dst,)

dst2=cv2.GaussianBlur(image,(5,5),sigmaX=7)#sigmax ve sigma y eksenlerin standart sapmasıdır
plt_imshow(dst2,"gaussian")

dst3=cv2.medianBlur(image,5)# medaian blur uygulandı
plt_imshow(dst3,"medianblur")

def gaussian_noise(image):
    row,col,ch=image.shape#resmin shape i ayrıldı
    mean=0# ortalama
    var=0.05# varyans
    sigma=var**0.5

    gaussian=np.random.normal(mean,sigma,(row,col,ch))#gürültü oluşturuldu
    gaussian=gaussian.reshape(row,col,ch)# boyutlar güncellendi
    noisy=image+gaussian# gürültü ve resim birleştirilerek gürültülü bir resim elde edildi

    return noisy

image=cv2.imread("data\\manzara_constrat.jpg")
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)/255# değerleri 0 ile bir arasına çekerek normalize ettik bunun sebebi gürültüyü ekleyebilmek

plt_imshow(image)

gaussian_noise1=gaussian_noise(image)

plt_imshow(gaussian_noise1,"gaussian noise")

# kendi elimizle bir gürültü elde ettik şimdi o gürültüyü tekrardan blur ile gidereceğiz

gb=cv2.GaussianBlur(gaussian_noise1,(5,5),sigmaX=7)#sigmax ve sigma y eksenlerin standart sapmasıdır
plt_imshow(gb,"gaussian")

def saltpperNoise(image):#siyah beyaz noktacıklar ile kirlilik eklemek
    row,col,ch=image.shape#resmin shape i ayrıldı

    s_vs_p=0.5# tuz ve karabiberin yani siyah ve beyazın oranını yazdık3
    amount=0.004
    noisy=np.copy(image)
    
    num_salt=int(np.ceil(amount*image.size *s_vs_p))# ceil fonksiyonu sayılarin virgülden sonraki ilk basamağını yuvarlar 1.1-1--- burada beyaz noktaların sayısı belirlendi
    coords = [np.random.randint(0,i-1,num_salt) for i in image.shape]# random ile kordinatlar belirlendi
    noisy[coords]=1# belirlenen sayıdaki random kordinatlar beyaz ayarlandı

    num_pepper=int(np.ceil(amount*image.size *s_vs_p))# ceil fonksiyonu sayılarin virgülden sonraki ilk basamağını yuvarlar 1.1-1--- burada beyaz noktaların sayısı belirlendi
    coords = [np.random.randint(0,i-1,num_pepper) for i in image.shape]# random ile kordinatlar belirlendi
    noisy[coords]=0# belirlenen sayıdaki random kordinatlar beyaz ayarlandı
    
    return noisy

sltppr_image=saltpperNoise(image)

plt_imshow(sltppr_image,"salt_paper_image")# nokta şeklinde kirliliği olan bir resim elde edildi

mb=cv2.medianBlur(sltppr_image.astype(np.float32),5)# medaian blur uygulandı
plt_imshow(dst3,"medianblur")#
