# resim ve klasörlere erişim
import glob
import os
import matplotlib.pyplot as plt
import numpy as np 
# derin öğrenme
from keras.models import Sequential
from keras.layers import Dense,Dropout,Flatten,Conv2D,MaxPooling2D
#dense: fully connected layer ,dropout:seyreltme,flatten:düzleştirme,
#convolutinal 2d :evrişim ağı ,maxpooling:piksel ekleme
from PIL import Image
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
import seaborn as sns
import pandas as pd
# uyarıları kaldırmak için:
import warnings
# uyarılar filtrelendi
warnings.filterwarnings("ignore")

imgs = glob.glob("img/*.png")# tüm png leri çe

width=125
height=50
X=[]
Y=[]

for img in imgs:
    filename=os.path.basename(img)# resmin yolu alındı
    #resim isminin baştaki up down kısımlarını alır
    label=filename.split("_")[0]
    #resimler yeniden boyutlandırılır
    im=np.array(Image.open(img).convert("L").resize((width,height)))
    #resimler 0 ile 1 arasında değer alması için normalize edilir
    im=im/255
    #resimler ve etiketler X ve Y ye eklendi
    X.append(im)
    Y.append(label) 

X=np.array(X)
# 1 parametresi keras için koyulacak
X=X.reshape(X.shape[0],width,height,1)  

#veriseti görselleştirmesi
#sns.countplot(y=Y)
#plt.show()

#etiketler nümerik hale gelir(0,1,2)
def onehot_labels(values):
    label_encoder=LabelEncoder()
    #öğrenme ve dönüştürme işlemleri 
    integer_encoded=label_encoder.fit_transform(values)
    onehot_encoder=OneHotEncoder(sparse=False)
    #integer encodedı (xx,1 haline getirdik)- bu kısım hatadan kaçınmak için yapıldı
    integer_encoded=integer_encoded.reshape(len(integer_encoded),1)
    onehot_encoded=onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoded 

Y=onehot_labels(Y)
#verisetini eğitim ve test olarak ayırırız
train_X,test_X,train_Y,test_Y=train_test_split(X,Y,test_size=0.25,random_state=2)

#CNN model inşası

#katmanları üzerine ekleyeceğimiz temel yapı 

model=Sequential()
#modele katman eklenir
model.add(Conv2D(32,kernel_size=(3,3),activation="relu",input_shape=(width,height,1)))
#inputu ilk katmanda belirtmem yeterli 
model.add(Conv2D(64,kernel_size=(3,3),activation="relu"))
#piksel ekleme 
model.add(MaxPooling2D(pool_size=(2,2)))
#seyreltme
model.add(Dropout(0.25))
#düzleştirme
model.add(Flatten())

#sınıflandırma

#ilk gizli katman
model.add(Dense(128,activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(3,activation="softmax"))
#softmax birden fazla sınıfın olduğu çıktılar için kullanılan bir aktivasyon fonksiyonudur

#hata fonksiyonu 
model.compile(loss='categorical_crossentropy',optimizer="Adam",metrics=["accuracy"])
#kayıp fonksiyonu ile çıkan hatalar ile ağırlıklar gün

#eğitim
model.fit(train_X,train_Y,epochs=35,batch_size=64)
#epoch ile kaç kere eğitim yapılması gerektiği 
#batch size ile ise her iterasyonda verisetinden kaçlık bir grup almamız gerektiği belirtilir

score_train=model.evaluate(train_X,train_Y)
print("eğitim doğruluğu:",score_train[1]*100) 
# score_train[0]= kayıp,[1]=accuracy-doğruluk

score_test=model.evaluate(test_X,test_Y)
print("test doğruluğu:",score_test[1]*100) 

#ağırlıklar kaydolur
open("model.json","w").write(model.to_json())
model.save_weights("trex_weight_newest.h5")