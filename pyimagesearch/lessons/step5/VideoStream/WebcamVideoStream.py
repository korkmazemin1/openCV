from threading import Thread
import cv2

class WebcamVideoStream :
    def __init__(self,src=0): # src videonun yolunu belirtir 0 birincil kamerea, 1 ikincil kamera olur ayrıca bir video yolu da girilebilir
        
        self.stream = cv2.VideoCapture(src)# kaynak belirtilerek video çekilir
        (self.grabbed,self.frame) =self.stream.read()# video okunur

        self.stopped=False# frame okumanın durup durmamasına karar verilir


    def start(self):
        Thread(target=self.update,args=()).start()# update ile yani bir sonraki kareyi çağıran fonksiyonu çağırarak start fonksiyonu hazırlandı

        return self    
    
    def update(self):# update ve start fonksiyonların ayrı ayrı yazılması fps arttırmamızı sağlar
        while True:
            if self.stopped:# eğer bir sonraki kare bulunmuşsa döngüyü durdur
                return
            
            (self.grabbed,self.frame)= self.stream.read()# eğer bulunamamış ise diğer kareyi çek

    def read(self):
        return self.frame # en son okunan fonksiyonu döndürür

    def stop(self):

        self.stopped=True     # classı hazırlarken yazdığımı durdurma işlevini çağıran fonksiyon


            
