from collections import deque
from threading import Thread
from queue import Queue
import time 
import cv2

class KeyClipWriter:
        def __init__(self, bufSize=64, timeout=1.0):# buffsize belirlendi --buffsize=arabellek boyutu  anlık kullanılan bellek olarak ele al
            
            self.bufSize = bufSize # önbelleğe alınabilecek maksimum kare sayısı
            self.timeout = timeout # yazılmaya hazır kare yokken beklenen zaman
            
            self.frames = deque(maxlen=bufSize) # en son okunan kare yanı kuyruğun sonu ve parametre olarak max uzunluk dönüyor
            self.Q = None # fifo(first-in-first-out) kuyruk yapısı ile yazılmayı bekleyen kareleri temsil eder
            self.writer = None # çıktı kısmına videoyu yazacak cv2.videowriter ın örneği
            self.thread = None #  maliyetli I/O dan kaçınmak adına video yazarken kullanacağımız iş parçacığı 
            self.recording = False # kayıt yapılmadığını sorgulayan bool    
        
        def update(self,frame):
            self.frames.appendleft(frame)
		
            if self.recording:# eğer kayıt yapılıyor ise kuyruğa ekle
                self.Q.put(frame)

        def start(self,outputPath,fourcc,fps):
             self.recording =True # kayıt işleminin devam ettiğini belirtir
             self.writer = cv2.VideoWriter(outputPath,fourcc,fps,(self.frames[0].shape[1],self.frames[0].shape[0]),True)# videoyu kaydetmek için parametreler girildi
             self.Q =Queue() # kuyruğu başlattık daha sonra tüm kareler arabelleğe atıp oradan kuyruğa ekleyeceğiz
             for i in range(len(self.frames),0,-1):# kareleri sondan başa doğru döndüren for döngüsü
                  self.Q.put(self.frames[i-1])# kareleri kuyruğa ekledik
                                           
             
             self.thread =Thread(target=self.write,args=())# write fonksiyonunu çağıran bir thread
             self.thread.daemon =True# deamon arka planda çalışan ve program başlamadan işini bitirmeyen bir iş parçacığı--thread--
             self.thread.start()# thread başlatıldı    -- iş parçacığı--   

        def write (self):
             while True:
                  if not self.recording:# kayıt bittiyse çık
                       return     
                  
                  if not self.Q.empty():
                       frame =self.Q.get()# kuyruktaki kare alındı
                       self.writer.write(frame)  # kare yazıldı


                  else :# eğer kuyrukta yazılmayı bekleyen bir kare yoksa beklemeye al
                       time.sleep(self.timeout)     

        def flush(self):

            while not self.Q.empty():# kaydetme işi bittiğinde kuyruğu boşaltmak için kullanılan fonksiyon
                 frame = self.Q.get()
                 self.writer.write(frame)

        def finish(self):
             self.recording =False# kaydır durdur
             self.thread.join()# iş parçacığı ana dosya ile birleşir
             self.flush()
             self.writer.release()# write komutu biter

