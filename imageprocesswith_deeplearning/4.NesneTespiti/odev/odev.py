import cv2
import numpy as np
import matplotlib.pyplot as plt
import os 


image=cv2.imread("pedestrian.jpg",0)#resim siyah beyaz olarak okundu

edges=cv2.Canny(image,threshold1 =0 , threshold2 = 255)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# thresold uygulanmadığında girinti ve çıkıntı dahil tüm kenarları aldı
cv2.waitKey()

median_value=np.median(image)# optimal threshold için medin değeri çekildi
print(median_value)

low=int(max(0,(1-0.33)*median_value))
high=int(max(0,(1+0.33)*median_value))
edges=cv2.Canny(image,threshold1 =low , threshold2 = high)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# kursta optimal olduğu belirtilen threshold parametreleri işe yaramadı
cv2.waitKey()
median_value=np.median(image)# optimal threshold için medin değeri çekildi
print(median_value)

low=int(max(0,(1-0.33)*median_value))
high=int(max(0,(1+0.33)*median_value))
blurred=cv2.blur(image,(5,5))
edges=cv2.Canny(image,threshold1 =low,threshold2 = high)# kenarlaraı tespit etmek için canny fonksiyonu kullanıldı threshold alınmadı
cv2.imshow("edges",edges)# kursta optimal olduğu belirtilen threshold parametreleri işe yaramadı
cv2.waitKey()#median value yönteminin pek bir işe yaramadığı gözlemlendi



face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")# cascade çekildi



def detect_face(img):
    face_img=img# fotonun kopyasını aldık

    face_recs=face_cascade.detectMultiScale(face_img)# cascade ile tespit yapıldı

    for (x,y,w,h) in face_recs:# yüzlerin sırası ile değerleri döner
        cv2.rectangle(face_img,(x,y),(x+w,y+h),(255,255,0),7) # elde edilen konumlar ile tespit edilen yüzlere dörtgenler çizildi

    return face_img


image=cv2.imread("pedestrian.jpg",0)

image=detect_face(image)
cv2.imshow("detect_face",image)
cv2.waitKey()
    

image=cv2.imread("pedestrian.jpg",0)

files=os.listdir()
img_path_list=[]
for file in files:
    if file.endswith(".jpg") :
        img_path_list.append(file)
print(img_path_list)

hog=cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())# insanları tespit eden hog

for image_path in img_path_list:
    print(image_path)
    image=cv2.imread(image_path)
    (rects,weights)=hog.detectMultiScale(image,padding=(8,8),scale=1.05)
    for (x,y,w,h) in rects:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
        
    cv2.imshow("yaya",image)    
    if cv2.waitKey(0) & 0xFF == ord("q"):continue
