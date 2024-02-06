# maksimum olmayan bastırma ile tespit edilen nesnelerden ihtimali yüksek olanlar seçilir
import numpy as np 
import cv2 

# saptanmak istenen nesne olma olasılığı yüksek olan pencere seçimi için bir algoritma
def non_maxi_suppression(boxes,probs=None,overlapThresh=0.3):
    
    # boş liste gelmesi halinde
    if len(boxes)==0:
        return []
    
    # integer veri gelmesi halinde floata dönüşüm yapılır
    if boxes.dtype.kind=="i":
        boxes=boxes.astype("float")

    #  bütün kutuların köşeleri  liste halinde çekildi
    x1=boxes[:,0]# her bir kutunun 0.elemanı yani x1 i
    y1=boxes[:,1]
    x2=boxes[:,2]
    y2=boxes[:,3]
 
    #alan bulma
    alan=(x2-x1+1)*(y2+y1+1)

    # y2 boş dönmemesi için atanan rastgele bir değer
    idxs=y2

    # olasılık değerleri 
    if probs is not None:
        idxs = probs 
       
    #olasılık sıralama
    idxs= np.argsort(idxs)
    
    #seçilen kutu 
    pick =[]
    while len(idxs)> 0:
        last = len(idxs)-1
        i=idxs[last]
        pick.append(i)

        # en büyük x ve y değerleri bulunacak 

        xx1=np.maximum(x1[i],x1[idxs[:last]])
        yy1=np.maximum(y1[i],y1[idxs[:last]])
        xx2=np.maximum(x2[i],x2[idxs[:last]])
        yy2=np.maximum(y2[i],y2[idxs[:last]])
        
        # genişlik ve yükseklik bulma 

        w=np.maximum(0,xx2-xx1+1)
        h=np.maximum(0,yy2-yy1+1)

        # overlap IoU(ıntersection over union)

        overlap=(w*h)/alan[idxs[:last]]
        # belirli bir değerin altında kalan kutular silinir
        
        idxs=np.delete(idxs,np.concatenate(([last],np.where(overlap>overlapThresh)[0])))
    return boxes[pick].astype("int")




