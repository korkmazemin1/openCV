import cv2



cascade=cv2.CascadeClassifier("cascade.xml")#göz için haarcascade





vid=cv2.VideoCapture(0)
#vid=cv2.VideoCapture(0)

while 1 :
    ret,frame=vid.read()
    frame=cv2.resize(frame,(480,360))

    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    body=cascade.detectMultiScale(gray,1.4,1)


    for (x,y,w,h)in body:
        cv2.rectangle(frame,(x,y),(y+h,x+w),(30,23,132),3)
    
    cv2.imshow("video_detect_eye",frame)

    if cv2.waitKey(20) & 0xFF==ord('q'):
        break
vid.release()
cv2.destroyAllWindows()
