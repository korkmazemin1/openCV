import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_img():
    blank_img=np.zeros((600,600))# her pikseli siyah olan bir fotoğraf 
    font=cv2.FONT_HERSHEY_PLAIN
    cv2.putText(blank_img,text="EMIN",org=(200,300),fontFace=font,fontScale=5,color=(255,255,255),thickness=8)# siyah resmin üzerine beyaz emnin yazısı 
    return blank_img

def display(img):
    fig =plt.figure(figsize=(12,10))# resim yeniden boyutlandırılır
    ax=fig.add_subplot(111)
    ax.imshow(img,cmap="gray")# gray formata çevrildi
    plt.waitforbuttonpress()

img =load_img()
display(img)

kernel=np.ones((5,5),dtype= np.uint8)# kernel oluşturuldu

result=cv2.erode(img,kernel,iterations=1)# erode ile aşındırma işlemi gerçekleştiriyoruz

display(result)


img=load_img()

white_noise=np.random.randint(low=0,high=2,size=(600,600)) # 1 ve 0 lardan oluşan random bir arrau yaptık

display(white_noise)

white_noise=white_noise *255# 1 piksel değerlerini 255 yaptık

noise_img= white_noise + img # ilk fotoyu gürültü ekledik
display(noise_img)

opening=cv2.morphologyEx(noise_img,cv2.MORPH_OPEN,kernel)# gürültülü olan resmimizi gürültüden arındırdık

display(opening)


img=load_img()
# oluşturulan gürültü fotoğrafında beyazlar yani 1 ler -255 ile işaretlenir
# daha sonra resim ve gürültü birleştirildikten sonra gürültüdeki işaretlenmiş beyaz noktalar siayaha çevrilir
# böylelikle yazının içindeki beyazlara dokunmadan yazı kirli bırakılır ve kalan kirler temizlenir
black_noise=np.random.randint(low=0,high=2,size=(600,600))# 600 er piksellerden oluşan 0 ve 1 lerden oluşan dizi

print(black_noise)
black_noise = black_noise* -255# gürültü fotoğrafı

print(black_noise)
black_noise_img= img+black_noise# # gürültü fotoğrafı resim ile toplanır

print(black_noise_img)
black_noise_img[black_noise_img==-255] = 0 # işaretlenmiş olan beyaz noktalar siyah hale gelir

print(black_noise_img)
display(black_noise_img)

closing=cv2.morphologyEx(black_noise_img,cv2.MORPH_CLOSE,kernel)# morph close ile harflerin içindeki görüntüleri yok ederiz
# kernel değeri ile oynayarak daha iyi sonuçlar elde edilebilir
display(closing)

img=load_img()
gradient=(img,cv2.MORPH_GRADIENT,kernel)# harflerin köşeleri belirtilerek içleri boşaltıldı















