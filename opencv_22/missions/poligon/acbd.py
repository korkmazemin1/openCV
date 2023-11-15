import cv2
import numpy as np 
from math import dist 
import imutils
import time

cap=cv2.VideoCapture("data\\output\\project_new2.mp4")

while 1:
    ret,frame=cap.read()
    print(ret)
    while ret:
        cv2.imshow("frame",frame)
        cv2.waitKey(0)
    if cv2.waitKey(30) == 27:
            break    
    


cap.release()
cv2.destroyAllWindows()
