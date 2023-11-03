
import cv2
import numpy as np 
from math import dist 
import imutils
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
"""

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

"""
     
    
"""
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
"""
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
    return score 
    


def shot_finder(prev_frame,frame):
    img1=prev_frame
    img2=frame
    
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
            """
            M =cv2.moments(c)
            cX = int(M["m10"] / M["m00"]) 
            cY= int(M["m01"] / M["m00"])
            """
            cv2.drawContours(img2, [c], -1, (0, 255, 0), 2) 
            
            #center_shot=(cX,cY)
            """
            if i==0:
                    pass
            else: 
               
                cv2.imshow("shot_cordinate",img2)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
                print(f"cordinate1: {c[0][0]}") 
            i +=1    
            """
    shot_cordinate=c[0][0]
    
    
      
    return shot_cordinate        

   
"""
poligon_first=cv2.imread("data\\input\\1.png") 
poligon=cv2.imread("data\\input\\2.png") 

poligon1=poligon_first
poligon2=poligon_first     
poligon3=poligon                         
center,little_radius=radius_finder(poligon1)
big_radius=radius_finder1(poligon_first,center) 

shot_cordinate=shot_finder(poligon_first,poligon)
"""



#print(f"shot_cordinate : {shot_cordinate}")
#shot_score(shot_cordinate,little_radius,big_radius,center)


"""
if shot_center!=None:
    score=shot_score(center,little_radius,shot_center,big_radius)
else:
    print("there is no Shot")    
"""

cap=cv2.VideoCapture("data\\output\\project_new.mp4")
ret,first_frame=cap.read()
first_frame1=first_frame
cv2.imshow("first_frame",first_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()


center,little_radius=radius_finder(first_frame)
big_radius=radius_finder1(first_frame1,center) 

d=0
l=0
while 1:
    ret,frame=cap.read()
     
    if ret==True:
        if d!=0:
            frame_saver=frame.copy()
            
            shot_cordinate=shot_finder(prev_frame,frame)
            
            
            prev_frame=frame_saver#burada framein işlem görmemiş hali haydediliyor
            shot_score(shot_cordinate,little_radius,big_radius,center)
            cv2.imshow("frame",frame)
            time.sleep(5)
            print(f"L==={l}")
            l=l+1

        else:
            cv2.imshow("frame",frame)
            time.sleep(5)
            prev_frame=frame

            
        if cv2.waitKey(30) == 27:
            break
        
        
        d +=1
    else:
          break   
cap.release()
cv2.destroyAllWindows()     


