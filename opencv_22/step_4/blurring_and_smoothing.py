import cv2
import numpy as np 
import matplotlib.pyplot as plt

def load_img():
    img=cv2.imread("opencv_22\\step_4\\image.jpg").astype(np.float32)/255# resim okundu
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)# resim rgb renk uzayına çevrildi
    return img


def display_img(img):# resmi yeniden boyutlandırarak gösteren fonksiyon 
    fig=plt.figure(figsize=(12,10))# resmin boyutu belirlendi
    ax=fig.add_subplot(111)
    ax.imshow(img)
    plt.waitforbuttonpress()



i=load_img()
display_img(i)    

gamma=1/4# gama değeri düştükçe parlaklıka artar
result=np.power(i,gamma)# np power ile parlaklığı değiştirdik
display_img(result)

img=load_img()

cv2.putText(img,"heyo",(150,152),cv2.FONT_HERSHEY_PLAIN,4,(255,0,0),3)# belirlenen konuma yazı yazıldı
display_img(img)


blurred = cv2.blur(img,ksize=(5,5))# 5 e 5 lik bir kernel ile resise blur uygulandı
display_img(blurred)

median=cv2.medianBlur(img,5)# resime medianblur uygulandı -- medianblur resmi gürültülerden arındırır

display_img(median)

