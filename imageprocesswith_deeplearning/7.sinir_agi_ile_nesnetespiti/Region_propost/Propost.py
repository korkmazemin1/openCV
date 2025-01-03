from keras.applications.resnet import preprocess_input,ResNet50
from keras.utils import img_to_array
from keras.applications import imagenet_utils
import numpy as np 
import cv2
import sys
sys.path.append('..') # üst dizinden kod çağırmak için yapıldı
from maksimum_olmayan_bastirma.bastirma import non_maxi_suppression

def selective_search(image):
    print("selective search ")
    ss=cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

    ss.setBaseImage(image)

    ss.switchToSelectiveSearchQuality()

    print("Start")
    rects =ss.process()
    return rects[:1000]

model=ResNet50(weights="imagenet")
image=cv2.imread("..\\data\\animals.jpg")
image=cv2.resize(image,(400,400))
(H,W)=image.shape[:2]

rects=selective_search(image)


proposals = []
boxes = []
for (x,y,w,h) in rects:

    # genişlik ve yükseklik kontrol edilir resim 
    # üzerinde küçük bir tespit ise iterasyon pas geçilir
    if w/float(W)<0.1 or h/float(H) <0.1:
        continue

    # Resnet modeli için roileri ön işleme 
    roi = image[y:y+h,x:x+w]
    roi=cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)
    roi=cv2.resize(roi,(224,224))

    roi=img_to_array(roi)
    roi=preprocess_input(roi)

    proposals.append(roi)
    boxes.append((x,y,w,h))

proposals=np.array(proposals)

preds=model.predict(proposals)
preds=imagenet_utils.decode_predictions(preds,top=1)

labels={}
min_conf=0.8
for (i,p) in enumerate(preds):
    
    (_,label,prob)=p[0]

    # eşik değerinden yüksek olan tespitler listeye alındı
    if prob>= min_conf:
        (x,y,w,h)=boxes[i]
        box=(x,y,x+w,y+h)
        #sözlüğe labels key i eklendi
        L=labels.get(label, [])
       
        L.append((box,prob))
        labels[label]=L
clone=image.copy()
for label in labels.keys():
    
    for (box,prob) in labels[label]:
    # non-maxima
        boxes=np.array([p[0] for p in labels[label]])
        probs=np.array([p[1] for p in labels[label]])
        boxes=non_maxi_suppression(boxes=boxes,probs=probs,overlapThresh=0.2)
        #overlapThresh bir hiperparamatredir 0.2 nin üstünde düzgün filtreleme yapılmaz 
        # ayrıntıları için import edilen fonksiyona gidebilirsin
      
        for (startX,startY,endX,endY) in boxes:
            cv2.rectangle(clone,(startX,startY),(endX,endY),(0,255,0),2)
            y=startY-10 if startY-10 >10 else startY+10
            cv2.putText(clone,label,(startX,y),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,0),2)
        cv2.imshow("maxima",clone)
        if cv2.waitKey(1) & 0xFF ==ord("q"):break    