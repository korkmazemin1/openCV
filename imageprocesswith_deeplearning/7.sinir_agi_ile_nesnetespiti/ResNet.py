from keras.applications.resnet import preprocess_input,ResNet50
from keras.utils import img_to_array
from keras.applications import imagenet_utils
import numpy as np 
import cv2
# daha önceden yazdığımız kodları çağırdık
from kayan_pencere.pencere import sliding_window
from piramit_gosterimi.piramit import image_pyramid
from maksimum_olmayan_bastirma.bastirma import non_maxi_suppression

WIDTH =600
HEIGHT =600
#resim piramidinin ölçütü
PYR_SCALE=1.5
#Pencerede kaç piksel atlanacağı
WIN_STEP=16
ROI_SIZE=(200,150)
#Resnet için input değeri 
INPUT_SIZE=(224,224)

print("ResNet yükleniyor...")
# Resnet yüklemesi
model=ResNet50(weights="imagenet",include_top=True)
#resim yüklendi
orig=cv2.imread("data\\husky3.jpg")

# Orjinal resmin boyutu ayarlandı
orig=cv2.resize(orig,dsize=(WIDTH,HEIGHT))


(H,W)=orig.shape[:2]
rois= []
locs= []
# resim boyutlandırma için piramit gös
pyramid=image_pyramid(orig,scale=PYR_SCALE,minSize=ROI_SIZE)

# her boyutta foto için piramit yöntemi kullanılır
for image in pyramid:
    scale=W/float(image.shape[1])
    
    for (x,y,roiOrig) in  sliding_window(image,WIN_STEP,ROI_SIZE):
        
        
        x= int(x*scale)
        y= int(y*scale)
        w= int(ROI_SIZE[0]*scale)
        h= int(ROI_SIZE[1]*scale)

        # resnete girecek olan görseller input size a getirilir
        roi=cv2.resize(roiOrig,dsize=INPUT_SIZE)
        
     # dizi haline getirilir
        roi=img_to_array(roi)
        
        # ve ön işlemeye alınır
        roi=preprocess_input(roi)
        # hatırlatma!! listeye yalnızca bir eleman ekleyebilirsi 
        rois.append(roi)
        locs.append((x,y,x+w,y+h))
 
rois =np.array(rois,dtype="float32")

#sınıflandırma kısmı 
print("siniflandirma yapiliyor")
# tahminler yapıldı 

preds=model.predict(rois)
# tahminler decode edilri
preds=imagenet_utils.decode_predictions(preds,top=1)


# tahminler eşik değerine çekilir
min_conf=0.9
labels={}
for (i,p) in enumerate(preds):
    
    (_,label,prob)=p[0]

    # eşik değerinden yüksek olan tespitler listeye alındı
    if prob>= min_conf:
        box=locs[i]
        #sözlüğe labels key i eklendi
        L=labels.get(label, [])
       
        L.append((box,prob))
        labels[label]=L

for label in labels.keys():
    clone = orig.copy()
    for (box,prob) in labels[label]:
        (startX,startY,endX,endY)=box
        # tespit edilen cisim için dörtgen çizilir
        cv2.rectangle(clone,(startX,startY),(endX,endY),(0,255,0),2)      

    cv2.imshow("ilk",clone)
    cv2.waitKey()

    clone=orig.copy()

    # non-maxima
    boxes=np.array([p[0] for p in labels[label]])
    probs=np.array([p[1] for p in labels[label]])
    box=non_maxi_suppression(boxes=boxes,probs=probs,overlapThresh=0.2)
    #overlapThresh bir hiperparamatredir 0.2 nin üstünde düzgün filtreleme yapılmaz 
    # ayrıntıları için import edilen fonksiyona gidebilirsin
    print(boxes)
    print(box)
    for (startX,startY,endX,endY) in box:
        cv2.rectangle(clone,(startX,startY),(endX,endY),(0,255,0),2)
        y=startY-10 if startY-10 >10 else startY+10
        cv2.putText(clone,label,   (startX,y),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,0),2)
    cv2.imshow("maxima",clone)
    cv2.waitKey()    

    

   