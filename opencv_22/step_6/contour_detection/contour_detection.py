import numpy as np 
import cv2
import matplotlib.pylab as plt

shapes=cv2.imread("images\\input\\internal_external.jpg")# resimler okundu
#shapes=cv2.bitwise_not(shapes)# kurs çıktısı ile yakın gitmek adına siyah beyaz değiştirildi
shapes=cv2.cvtColor(shapes,cv2.COLOR_BGR2GRAY)
shapes=cv2.blur(shapes,(11,11))

contours,hierarchy =cv2.findContours(shapes,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)#retr parametresi konturları içten mi dışttan mı bakıldığını sorgulayan parametre bu parametre dıştan alır
# hierarchydeki -1 ler bize dışbükey konturları verir
print(len(contours))

external_counters=np.zeros(shapes.shape)# her elemanı sıfır olan fotomuz boyutunda bir foto oluşturur


for i in range (len(contours)):
    if hierarchy[0][i][3]==-1:# yukarıda bahsettiğimiz dışbükey noktaları belirten eksi 1 lerin olması durumunda:
       cv2.drawContours(external_counters,contours,i,255,-1) # koşulları sağlayan aldığımız veriler ile konturlar çizilir

cv2.imshow("kontur",external_counters)
cv2.waitKey(0)
cv2.destroyAllWindows()


image_internal=np.zeros(shapes.shape)

for i in range (len(contours)):
    if hierarchy[0][i][3]!=-1:# burada ise içbükey şekilleri hierarchy ile bulma koşulu verilmiştir
        cv2.drawContours(image_internal,contours,i,255,-1)

cv2.imshow("kontur",image_internal)
cv2.waitKey(0)
cv2.destroyAllWindows()