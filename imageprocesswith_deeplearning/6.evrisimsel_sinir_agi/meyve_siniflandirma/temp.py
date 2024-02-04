# resim ve klasörlere erişim
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np 
# derin öğrenme
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D,BatchNormalization
#dense: fully connected layer ,dropout:seyreltme,flatten:düzleştirme,
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
#convolutinal 2d :evrişim ağı ,maxpooling:piksel ekleme
from PIL import Image
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
# uyarıları kaldırmak için:
import warnings
# uyarılar filtrelendi
import seaborn as sns
from tqdm import tqdm

#veri yolu verildi
path_train="data\\new_Train"
path_test="data\\new_Test"
#dosyalar liste haline getirildi
train_list=os.listdir(path_train)
test_list=os.listdir(path_test)

noOfClasses=len(train_list)


className= []

def image_process(path):
    images =[]
    className= []
    x=0
    for  i in tqdm(range(noOfClasses)):
        #klasörlerin içine direkt erişim için path ile sayı eklendi
        myImageList = os.listdir(path)
        for label in tqdm(myImageList):    
            for j in os.listdir(path+"\\"+label):
                #data içerisindeki fotoğraflara erişim sağladık
                
                
                img=cv2.imread(path+"\\"+str(label)+"\\"+str(j))
               
                img=cv2.resize(img,(32,32))
                images.append(img)
                className.append(label)
        ###resimlere ön işleme yapılır
        images=np.array(images)
        #sınıf numaraları tek bir listede
        className=np.array(className)
        return images[100],className[100]
img,cls=image_process(path_train)
print(cls)
print(img.shape)
cv2.imshow("img",img)
cv2.waitKey()