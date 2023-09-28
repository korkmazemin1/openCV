import datetime

class FPS:
    def __init__(self):

        self._start=None
        self.__end=None
        self._numFrames= 0# fps classı için gerekli değişkenleri tanımladık

    def start(self):

        self._start=datetime.datetime.now()
        return self    # başlama süresi alınır
    
    def stop(self):# bitiş süresi alınır
        self._end = datetime.datetime.now()

    def update(self):
        self._numFrames+=1 
        #  başlama ve bitişinden ayrı olarak çalışan bir sonraki kareyi getiren fonksiyon--fps arttırmak için
    def elapsed(self):
        return (self._end-self._start).total_seconds()# bitiş ve başlangıç zamanları arasından geçen zamanı hesaplar-elapsed time-
    
    def fps (self):
        return self._numFrames/self.elapsed()# okunan kare sayısı ile geçen zamanı bölerek fps hesaplıyoruz
    

