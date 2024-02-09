import cv2 
import pickle 
import numpy as np 
import random
from  keras.preprocessing.image import img_to_array


image=cv2.imread("..\\data\\mnist.png")

# selective search uygulanır
# ilklendir ss
ss=cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()

ss.setBaseImage(image)

ss.switchToSelectiveSearchQuality()

print("Start")
rects=ss.process()

boxes= []
proposals = []
output=image.copy()
# kareler tek tek sınıflandırılır
for (x,y,w,h) in rects[:10]:
    color = [random.randint(0,255) for j in range(0,3)]
    cv2.rectangle(output,(x,y),(x+w,y+h),color,2)
    # roi belirlenir
    roi=image[y:y+h,x:x+w]
    # roi yeniden boyutlandırılır
    ###
    roi=cv2.resize(roi,(32,32),interpolation=cv2.INTER_LANCZOS4)
    roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)

    roi=img_to_array(roi)
    proposals.append(roi)
    boxes.append((x,y,w+x,h+y))
proposals=np.array(proposals,dtype="float32")
boxes=np.array(boxes,dtype="int32")

pickle_in=open("model_trained_v4.p","rb")
model=pickle.load(pickle_in)
print("tahmin")
probs = model.predict(proposals)

number_list=[]
idx=[]
print("sınıflandırma")
for i in range (len(probs)):
    max_prob=np.max(probs[i,:])
    if max_prob>0.95:
        idx.append(i)
        number_list.append(np.argmax(probs[i]))

# tespit edilen kutular yazdırılır
for i in range(len(number_list)):
    j=idx[i]
    cv2.rectangle(image,(boxes[j,0],boxes[j,1]),(boxes[j,2],boxes[j,3]),(0,0,255),2)
    cv2.putText(image,str(np.argmax(probs[j])),(boxes[j,0]+5,boxes[j,1]+5),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),1)
    cv2.imshow("image",image)
    cv2.waitKey()