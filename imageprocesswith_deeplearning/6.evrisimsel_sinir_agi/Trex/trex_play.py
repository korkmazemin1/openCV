from keras.models import model_from_json
import numpy as np 
from PIL import Image
import keyboard
import time
from mss import mss

# trex oyununun pikselleri
mon={"top":468,"left":644,"width":250,"height":130}
sct=mss()

width=125
height=50

#model yükleme

model=model_from_json(open("model.json","r").read())#model okundu
model.load_weights("trex_weight_newest.h5")

#down =0 ,right=1,up=2

labels = ["Down","Right","Up"]

framerate_time =time.time()
counter=0
i=0
delay=0.4
key_down_pressed=False

while True:
    img=sct.grab(mon)
    #dönüşümler
    im=Image.frombytes("RGB",img.size,img.rgb)
    im2=np.array(im.convert("L").resize((width,height)))
    #normalize
    im2=im2/255

    X=np.array([im2])
    #girdi değerlerine göre resize edildi
    X=X.reshape(X.shape[0],width,height,1)
    r=model.predict(X)

    result=np.argmax(r)
    #[0.2,0.3,0.5] gibi bir dizideki en büyük sayının indeksini alır
    #softmax

    if result==0:
        # aşağı etiketi gelirse aşağı tuşuna bas
        keyboard.press(keyboard.KEY_DOWN)
        key_down_pressed=True
    elif result==2:
        if key_down_pressed:
            keyboard.release(keyboard.KEY_DOWN)
        time.sleep(delay)
        keyboard.press(keyboard.KEY_UP)
        # oyundaki huza bağlı olarak time sleep gerçekleşir
        if i<=1500:
            time.sleep(0.3)
        elif 1500<=i and i<=5000:
            time.sleep(0.13)     
        else :
            time.sleep(0.10)       

        keyboard.press(keyboard.KEY_DOWN)
        # alt tuşunu bırak
        keyboard.release(keyboard.KEY_DOWN)

        if (time.time()-framerate_time) >= 1:
            
            counter = 0 
            framerate_time=time.time()
            if i <=1500:
                delay-=0.003
            else:
                delay -=0.005
            if delay<=0:
                delay=0
            print("----------------")
            print(f"Down: {r[0][0]} \nRight: {r[0][1]} \nUp: {r[0][2]}")    
            i +=1        