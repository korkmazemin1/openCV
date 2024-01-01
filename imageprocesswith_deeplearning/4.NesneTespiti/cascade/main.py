import numpy as np
import cv2 
from matplotlib import pyplot as plt
import os
path="images"

#resim boyutu

imgwidth=180
imgheight=120

cap=cv2.VideoCapture(0)# webcam açıldı
cap.set(3,640)#kameramızın pikseli 
cap.set(4,480)#640x480
cap.set(10,180)# kameranın aydınlık seviyesi

global countfolder
def saveDataFunc():
    global countfolder
    countfolder=0
    while os.path.exists(path+str(countfolder)):
        countfolder+=1
    os.makedirs(path+str(countfolder))  #dosya sayılır



saveDataFunc()

count=0
countSave=0
while True:
    success,img =cap.read()
     
    if success:
        img=cv2.resize(img,(imgwidth,imgheight))# frameler yeniden boyutladnırıldı

        if count %5 ==0:# aynı görselleri almamak için 5 in modunu aldık
            cv2.imwrite(path+str(countfolder)+"/"+ str(countSave)+"_"+".png",img)
            countSave +=1
            print(countSave)
        count +=1

        cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF ==ord("q"):break
cap.release()
cv2.destroyAllWindows()



           


