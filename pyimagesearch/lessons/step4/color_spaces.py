import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, default="adrian.png",help="girilecek resmin yolu")
	    
args = vars(ap.parse_args())

# komut satırı işlemleri

image=cv2.imread(args["image"])
cv2.imshow("RGB",image)

for (name,chan) in zip(("B","G","R"),cv2.split(image)):# bu döngü ile resmin rgb tonları sırası ile gösterilir
    cv2.imshow(name,chan)# yukarıdaki split fonksiyonu bgr ı sırası ile ayrıştırı ve gösterir

cv2.waitKey(0)
cv2.destroyAllWindows()

hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
cv2.imshow("HSV",hsv)# resim bgr formatından hsv formatına çevrildi

for (name,chan) in zip(("H","S","V") ,cv2.split(hsv)):# dögü h-s-v kanallarını ayrı ayrı gösterir
    cv2.imshow(name,chan)

cv2.waitKey(0)
cv2.destroyAllWindows()

lab=cv2.cvtColor(image,cv2.COLOR_BGR2LAB)# görüntü lab formatına çevrildi ve görüntülendi
cv2.imshow("L*a*b*",lab)

for(name,chan) in zip(("L*","b*","a*"),cv2.split(lab)):# l-a-b kısımları split fonksiyonu ile ayrı ayrı görüntülendi
    cv2.imshow(name,chan)

cv2.waitKey(0) 
cv2.destroyAllWindows()   

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi
cv2.imshow("original",image),
cv2.imshow("Grayscale",gray)
cv2.waitKey(0),
cv2.destroyAllWindows()