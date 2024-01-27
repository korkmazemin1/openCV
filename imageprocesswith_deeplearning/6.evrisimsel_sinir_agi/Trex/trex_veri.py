import keyboard
import uuid
from PIL import Image
import time 
from mss import mss


# roi belirlenir
mon={"top":468,"left":644,"width":250,"height":130}

# ekrandan belirtilen roiyi çekecek kütüphane fonksiyonu 
sct=mss()
i=0
def recrod_screen(record_id,key):
    global i 

    # i klavyeyi kaç kez bastığımızı sayar
    i +=1
    print(f"{key}:{i}")
    # belirlenen kısmı çek
    img=sct.grab(mon)
    #rgb formatında okuma
    im=Image.frombytes("RGB",img.size,img.rgb)
    # belirtilen yola ve isime resimleri kaydeder
    im.save(f"img/{key}_{record_id}_{i}.png")

is_exit=False

# fonksiyondan çıkış için exit fonksiyonu
def exit():
    global is_exit
    is_exit=True
#klavyeden esc girilince exit fonksiyonu çağrılır    
keyboard.add_hotkey("esc",exit)    

record_id=uuid.uuid4()#id belirlendi

while True:
    if is_exit:break

    try:
        # tuşa basıldığında
        if keyboard.is_pressed("up"):
            recrod_screen(record_id,"up")
            #hızı kontrol etmek adın time kullanılır
            time.sleep(0.1)
        elif keyboard.is_pressed("down"):
            recrod_screen(record_id,"down")   
            time.sleep(0.1) 
        #zıplamamsı gereken yerlerde bu tuşa basılacak ve negatif veri çekilecek
        elif keyboard.is_pressed("right"):
            recrod_screen(record_id,"right") 
            time.sleep(0.1)
    except RuntimeError:  continue      