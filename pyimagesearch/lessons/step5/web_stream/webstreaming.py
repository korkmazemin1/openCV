from simplemotiondetector import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2


outputFrame= None# websitesinde göstreilecek kare 
lock =threading.Lock()

app=Flask(__name__) # uygılamayı belirledik

vs=VideoStream(src=0).start()#video okumak için kaynak belirlendi
time.sleep(2.0)

@app.route("/")
def index():
	
	return render_template("index.html")# html dosyasını taramak için 

def detect_motion(frameCount):
	
    global vs,outputFrame,lock# güncel video ,gösterilecek kare,güncellemeden önce alınması gereken kilit

    md=SingleMotionDetector(accumWeight=0.1) # değeri daha yüksek ağırlıklandırmak için düşük bir birikimli ağırlık değeri girildi

    total=0

    while True:
		
        frame = vs.read()# resim okundu
        frame = imutils.resize(frame, width=400)# yeniden boyutlandırdı
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)# gray formata çevrildi
        gray = cv2.GaussianBlur(gray, (7, 7), 0)# blur uygulandı
		
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)



        if total > frameCount:# arka plan tespiti için yeterli frame oluştuktan sonra 
            motion =md.detect(gray)  # framelere işlem uygulanmaya başlar

            if motion is not None:# eğer hareket tespit edildi ise
                 
                (thresh,(minX,minY,maxX,maxy)) =motion  
                cv2.rectangle(frame,(minX,minY),(maxX,maxX),(0,0,255),2)#tespit edilen nesnenin etrafına dörtgen çizimi
        md.update(gray)
        total +=1 

        with lock:
             outputFrame=frame.copy()   #frame i elde ettikten sonra kilit kaldırılır    ,

def generate():
     global outputFrame,lock # globaldeki outputu ve kilit değişkenlerini çağırdık

     while True:
          with lock:#kilidi kaldır
                if outputFrame is None: # output frama müsait ise 
                    continue# değilse geç

                (flag,encodedImage)=cv2.imencode(".jpg",outputFrame)# kareleri jpeg formatına çevirdik


                if not flag: # karelerin doğru şekilde jpege çevrildiğini kontrol et
                     continue
                                  

             
          yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')  # çıktı çerçevesini byte şeklinde verir-- web sayfasının okuyabilmesi için  

@app.route("/video_feed")# verilerin bu uç adresde olduğunu fluska bildirir
def video_feed():
	# burada flask ile bağlantı kuruldu
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ =="__main__":
	
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    t = threading.Thread(target=detect_motion, args=(args["frame_count"],)) #  hareket tespitini yapan fonksiyonununu işlemek için bir iş parçacığı açıldı
    t.daemon = True
    t.start()

    app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)# flask çalıştırıldı
    

vs.stop()    # videostrema durduruldu