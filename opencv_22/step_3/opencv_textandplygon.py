import cv2
import numpy as np
import matplotlib.pyplot as plt

empty_foto=np.zeros(shape=(512,512,3),dtype=np.int16)# siyah renginde 3 kanallı foto oluşturduk

cv2.putText(empty_foto,"Emin",(200,300),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2,(100,180,255))# girilen konum yazının nereden başladığını gösterir--beyaz renginde belirlediğimiz tipte yazı ekledik

points=np.array([[100,300],[254,132],[0,12],[12,0],[45,400]],dtype=np.int32)# polygon yani çokgen çizeceğimiz noktaları belirttik

cv2.polylines(empty_foto,[points],isClosed=True,color=(129,23,200),thickness=5)# is closed ile ilk ve son noktalarının kapanması boolunu True verdik 




plt.imshow(empty_foto)
plt.waitforbuttonpress()