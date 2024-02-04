import cv2
import pickle
import numpy as np 


# ön işleme
def preprocess(img):
    # siyah beyaza çevrildi
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #histogram eşitlendi
    img=cv2.equalizeHist(img)
    #normalizasyon
    img=img/255

    return img

cap=cv2.VideoCapture(0)
# genişlik ve yüksseklik
cap.set(3,480)
cap.set(4,480)
#model çekildi
pickle_in=open("model_trained_new.p","rb")
model=pickle.load(pickle_in)

while True:
    success,frame=cap.read()
    # ön işleme
    img=np.asarray(frame)
    img=cv2.resize(img,(32,32))
    img=preprocess(img)

    img=img.reshape(1,32,32,1)

    # tahmin
    
    predictions=model.predict(img)
    classIndex=np.argmax(predictions,axis=1)
    probval=np.amax(predictions)
    print(classIndex,probval)

    if probval >=0.55:
        cv2.putText(frame,str(classIndex)+"  "+str(probval),(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0),1)
    cv2.imshow("rakam siniflandırma:",frame)
    if cv2.waitKey(1) & 0xFF==ord("q"): break