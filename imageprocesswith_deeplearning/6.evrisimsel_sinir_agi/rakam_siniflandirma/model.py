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

#veri yolu verildi
path="myData"

#dosyalar liste haline getirildi
myList=os.listdir(path)
noOfClasses=len(myList)

images =[]
classNo= []

for  i in range(noOfClasses):
    #klasörlerin içine direkt erişim için path ile sayı eklendi
    myImageList = os.listdir(path+"\\"+str(i))
    for j in myImageList:
        #data içerisindeki fotoğraflara erişim sağladık
        img=cv2.imread(path+"\\"+str(i)+"\\"+j)
        img=cv2.resize(img,(32,32))
        images.append(img)
        classNo.append(i)

images=np.array(images)
#sınıf numaraları tek bir listede
classNo=np.array(classNo)


#veri ayırma
#veri bölündü
x_train,x_test,y_train,y_test=train_test_split(images,classNo,test_size=0.5,random_state=42)
#eğitim seti doğrulama için tekrardan ikiye bölündü
x_train,x_validation,y_train,y_validation=train_test_split(x_train,y_train,test_size=0.2,random_state=42)


"""
##veri görselleştirme
fig, axes = plt.subplots(3, 1, figsize=(7, 7))  # 3 satır, 1 sütunlu subplotlar oluştur

fig.subplots_adjust(hspace=0.5)

sns.countplot(y_train, ax=axes[0])
axes[0].set_title("y_train")

sns.countplot(y_test, ax=axes[1])
axes[1].set_title("y_test")

sns.countplot(y_validation, ax=axes[2])
axes[2].set_title("y_validation")
plt.show()
"""
#ön işleme

def preprocess(img):
    # siyah beyaza çevrildi
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #histogram eşitlendi
    img=cv2.equalizeHist(img)
    #normalizasyon
    img=img/255

    return img

#map yöntemi
# dizi içersindeki tüm resimler belirtilen fonksiyonun içine atıldı ve sonuçları kaydedildi
x_train=np.array(list(map(preprocess,x_train)))
x_test=np.array(list(map(preprocess,x_test)))
x_validation=np.array(list(map(preprocess,x_validation)))

x_train=x_train.reshape(-1,32,32,1)
#-1 parametresi dizide kaç tane sayı olduğunu temsil eder
x_test=x_test.reshape(-1,32,32,1)
x_validation=x_validation.reshape(-1,32,32,1)

# veri arttırma

dataGen=ImageDataGenerator(width_shift_range=0.1,height_shift_range=0.1,zoom_range=0.1,rotation_range=10)
# resimleri x,y ekseninde hareket ettirme ,yakınlaştırma,yönlendirme metodları ile arttırdık

dataGen.fit(x_train)

#classları kategorik hale getiriyoruz
# onehot encoder ile aynı işi yapıyor
y_train=to_categorical(y_train,noOfClasses)
y_test=to_categorical(y_test,noOfClasses)
y_validation=to_categorical(y_validation,noOfClasses)
print(y_train[0:100])

#cnn oluşturma


model=Sequential()
#giriş katmanları
model.add(Conv2D(input_shape=(32,32,1),filters=8,kernel_size=(5,5),activation="relu",padding="same"))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(filters=16,kernel_size=(5,5),activation="relu",padding="same"))
model.add(MaxPooling2D(pool_size=(2,2)))

#aşırı öğrenmeden kaçınmak için seyreltme uygulanır
model.add(Dropout(0.2))
model.add(Flatten())

#gizli katman
model.add(Dense(units=256,activation="relu"))
model.add(Dropout(0.2))
#çıkış katmanı

model.add(Dense(units=noOfClasses,activation="softmax"))

#kayıp fonksiyonu
model.compile(loss="categorical_crossentropy",optimizer=("Adam"),metrics=["accuracy"])

batch_size=250
#eğitim
hist=model.fit(x_train,y_train,batch_size,validation_data=(x_validation,y_validation),epochs=10,steps_per_epoch=x_train.shape[0]//batch_size,shuffle=1)
#hist=model.fit_generator(dataGen.flow(x_train,y_train,batch_size,validation_data=(x_validation,y_validation),epoch=15,steps_per_epoch=x_train.shape[0]//batch_size,shuffle=1))

#model depolama
pickle_out=open("model_trained_new.p","wb")
pickle.dump(model,pickle_out)
pickle_out.close()

#değerlendirme

# kayıp değerleri 
plt.figure()
plt.plot(hist.history["loss"],label="eğitim_kayip")
plt.plot(hist.history["val_loss"],label="doğrulama kayip")
plt.legend()
plt.show()


# doğruluk değerleri
plt.figure()
plt.plot(hist.history["accuracy"],label="eğitim doğruluk")
plt.plot(hist.history["val_accuracy"],label="doğrulama doğruluk")
plt.legend()
plt.show()

# test verileri ile tahminler yapılıp sonuçlar alınır
score=model.evaluate(x_test,y_test,verbose=1)
print("Test loss: ",score[0])
print("Test accuracy: ",score[1])

#doğrulama verisi ile tahminler alınır
y_pred=model.predict(x_validation)
# tahmin çıktıları incelenirse burada sınıflara değerler verilmiştir ve burada en yüksek değeri olan tahmindir
#bu nedenden argmax ile en yüksek değerin indexi alınıp tahmin olarak verilir
y_pred_class=np.argmax(y_pred,axis=1)

"""print("y_pred_class",y_pred_class[0])
print("y_pred",y_pred[0])"""

y_true=np.argmax(y_validation,axis=1)

# tahmin ve gerçek değerler karşılaştırılır ve confusion ile görselleştirilir
cm=confusion_matrix(y_true,y_pred_class)

f,ax=plt.subplots(figsize=(8,8))
sns.heatmap(cm,annot=True,linewidths=0.01,cmap="Greens",linecolor="gray",fmt=".1f",ax=ax)
plt.xlabel("predicted")
plt.ylabel("true")
plt.title("confussion matris")
plt.show()