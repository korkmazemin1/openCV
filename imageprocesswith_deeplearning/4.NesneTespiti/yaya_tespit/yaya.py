import os 
import cv2
files=os.listdir()
img_path_list=[]
for file in files:
    if file.endswith(".jpg") :
        img_path_list.append(file)
print(img_path_list)

hog=cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())# insanları tespit eden hog

for image_path in img_path_list:
    print(image_path)
    image=cv2.imread(image_path)
    (rects,weights)=hog.detectMultiScale(image,padding=(8,8),scale=1.05)
    for (x,y,w,h) in rects:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,255),2)
        
    cv2.imshow("yaya",image)    
    if cv2.waitKey(0) & 0xFF == ord("q"):continue
