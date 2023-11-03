import cv2
import numpy as np 
from math import dist 
import time
"""
cap=cv2.VideoCapture("data\\output\\project2.mp4")
def poligon_counter(img):
   
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  

   gray_blurred = cv2.blur(gray, (3, 3)) 
  
 
   detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 40)
   detected_circles = np.uint16(np.around(detected_circles)) 
  
   for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 

        cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
   return img
while 1:
    
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    
    gray = cv2.medianBlur(gray, 5)
    
    
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=30,
                               minRadius=1, maxRadius=30)
    
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(frame, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(frame, center, radius, (255, 0, 255), 3)
    cv2.imshow("frame",frame)

    
    
    if cv2.waitKey(20) == 27:
      break       
    time.sleep(3)
cap.release()
cv2.destroyAllWindows()    
"""

def radius_finder(poligon):
    gray = cv2.cvtColor(poligon, cv2.COLOR_BGR2GRAY)
    
    
    gray=cv2.medianBlur(gray,15)
    


    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 4,
                               param1=120, param2=50,
                               minRadius=5, maxRadius=70)
    
    
    if circles is not None:
        
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(poligon, center, 1, (255, 0, 0), 3)
            # circle outline
            radius = i[2]
            cv2.circle(poligon, center, radius, (255, 0, 255), 3)
            
            print(f"center: {center},radius: {radius}")
            
        #cv2.imshow("gray",gray)
    cv2.imshow("poligon",poligon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return center,radius

def shot_finder(point):
    lower_gray = np.array([0, 0, 127])
    upper_gray = np.array([0, 0, 127])

    hsv=cv2.cvtColor(point,cv2.COLOR_BGR2HSV)
    
    mask1=cv2.inRange(hsv,lower_gray,upper_gray)# 4 adımlı bir mask işlemi uygulandı
    blur=cv2.medianBlur(mask1,5)
    blur=cv2.bitwise_not(blur)

    contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#kontur bulma fonksiyonu


    cv2.drawContours(point,contours,1,(0,0,255),3)
    # momnets ile bulunan konturun merkezi hesaplanır
    for c in contours:
        M=cv2.moments(c)
    
        cX=int(M["m10"]/ (M["m00"] ))
        cY=int(M["m01"]/(M["m00"]))
        center=(cX,cY)
    print(center)
    cv2.circle(point,center,1,(255,0,0))    
    shot_center=center


    cv2.imshow("point",point)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"shot_center: {shot_center}")
    return shot_center

def shot_score(center,radius,shot_center):
    distance=dist(shot_center,center)

    if radius>= distance > 0:
        score=1
    elif 3*radius>= distance > radius:    
        score=2
    elif 5*radius>= distance > 33*radius:    
        score=3
    elif 7*radius>= distance > 5*radius:    
        score=4   
    elif 9*radius>= distance > 7*radius:    
        score=5 
    else :
        score=0
    print(f"your score is: {score}")
    print(f"distance: {distance}, center: {center}, shot_center: {shot_center},radius: {radius}")    
    return score


    


poligon=cv2.imread("data\\input\\1.png")   
center,radius=radius_finder(poligon) 

point=cv2.imread("data\\input\\2.png")
shot_center=shot_finder(point)
score=shot_score(center,radius,shot_center)

