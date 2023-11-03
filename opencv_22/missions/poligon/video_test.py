import cv2
import numpy as np 
from math import dist 
import imutils
import time

def radius_finder1(poligon,center):# çember hesabı yalnıza ilk frame ile yapılmalı
    min=10000000000
    gray = cv2.cvtColor(poligon, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    #result = 255 - thresh
    kernel=np.ones((5,5),np.uint8)
    dilation=cv2.dilate(thresh,kernel,iterations=2)
    eroision=cv2.erode(dilation,kernel,iterations=1)
    
    cv2.imshow("erosion",eroision)
    cv2.imshow("dilate",dilation)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
   

    #rows = gray.shape[0]
    edged = cv2.Canny(gray, 30, 200)
    cv2.imshow("edged",edged)

    contours,_=cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#kontur bulma fonksiyonu
    contours = list(filter(lambda cnt: cv2.contourArea(cnt)> 120, contours))# küçük noktalardan kaçınmak için kontur boyutları filtrelendi
    
    
    
    for c in contours:

        M =cv2.moments(c)
        cX = int(M["m10"] / M["m00"]) 
        cY= int(M["m01"] / M["m00"])

        cv2.drawContours(poligon, c, -1, (0, 255, 0), 2)
        
        print(f"c: {c[0][0]}")
        cv2.circle(poligon , (cX, cY), 7, (0, 255, 255), -1)
        
        test=dist(c[0][0],(0,0))
        
        if test<min:
            min=test
            cordinate=c[0][0]
            

    print(f"cordinate : {cordinate}")    
    cv2.circle(poligon,cordinate,5,(0,0,255),7)
    big_radius=dist(center,cordinate)

        

    cv2.drawContours(edged,contours,-1,(255,255,0),3)
    
    cv2.imshow("draw",edged)
    cv2.waitKey(0)

    cv2.imshow("poligon1",poligon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f"big_radius :{big_radius}")
    return big_radius

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
            little_radius=radius
            cv2.circle(poligon, center, radius, (255, 0, 255), 3)
            
            print(f"center: {center},radius: {radius}")
            
        #cv2.imshow("gray",gray)
    cv2.imshow("poligon",poligon)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return center,little_radius  

def shot_score(shot_cordinate,little_radius,big_radius,center):
    distance_shot=dist(center,shot_cordinate)
    gap_distance=(big_radius-little_radius)/4
    
    if distance_shot<=little_radius:
         score=1
    elif little_radius<=distance_shot<gap_distance+little_radius:
         score=2
    elif little_radius+gap_distance<=distance_shot<2*gap_distance+little_radius:
         score=3
    elif little_radius+2*gap_distance<=distance_shot<3*gap_distance+little_radius:
         score=4
    elif little_radius+3*gap_distance<=distance_shot<4*gap_distance+little_radius:
         score=5
    else:
         score=0
    print(f"your score is {score}",f"gap_distance :{gap_distance}",f"distance_shot : {distance_shot}")           

def shot_finder():
    img1=cv2.imread("data\\input\\4.png")
    img2=cv2.imread("data\\input\\5.png")

    abs=cv2.absdiff(img1,img2)
    gray_abs=cv2.cvtColor(abs,cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray_abs, 50, 255, cv2.THRESH_BINARY_INV) 
    thresh2 = cv2.adaptiveThreshold(gray_abs, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 199, 5) 

    contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, 
                                cv2.CHAIN_APPROX_NONE) 
    
    # take the first contour 
    i=0
    for c in contours:

            M =cv2.moments(c)
            cX = int(M["m10"] / M["m00"]) 
            cY= int(M["m01"] / M["m00"])

            cv2.drawContours(img2, [c], -1, (0, 255, 0), 2) 
            
            
            if i==0:
                    pass
            else: 
                cv2.imshow("shot_cordinate",img2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                print(f"cordinate1: {c[0][0]}") 
            i +=1    
    shot_cordinate=c[0][0] 
    
      
    return shot_cordinate     







cap=cv2.VideoCapture("data\\output\\project3.mp4")
ret,first_frame=cap.read()
first_frame1=first_frame
cv2.imshow("first_frame",first_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

center,little_radius=radius_finder(first_frame)
big_radius=radius_finder1(first_frame1,center) 


while 1:
     ret,frame=cap.read()
     if cv2.waitKey(30) == 27:
      break
     cv2.imshow("frame",frame)
     time.sleep(1)
cap.release()
cv2.destroyAllWindows()     