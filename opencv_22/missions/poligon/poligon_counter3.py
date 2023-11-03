import cv2
import numpy as np
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
    
    kernel=np.ones((3,3),np.uint8)
    
    #morfoloji2=cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel)
    #gray=cv2.medianBlur(morfoloji2,3)
    #cv2.imshow("morfoloji2",morfoloji2)
    dilate= cv2.dilate(gray, kernel, iterations=1) 
    
    gray=cv2.medianBlur(dilate,11)
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 199, 5) 
    cv2.imshow("thresh",thresh2)
    
    contours, _ = cv2.findContours(thresh2, cv2.RETR_TREE, 
                               cv2.CHAIN_APPROX_SIMPLE) 
    count = contours[0] 
    M = cv2.moments(count) 
    (x_axis,y_axis),radius = cv2.minEnclosingCircle(count) 
  
    center = (int(x_axis),int(y_axis)) 
    radius = int(radius) 
  
    cv2.circle(poligon,center,radius,(0,255,0),2) 
    #rows = gray.shape[0]
    """
    circles = cv2.HoughCircles(dilate, cv2.HOUGH_GRADIENT, 1, rows / 8,
                              # param1=50, param2=50,
                               #minRadius=250, maxRadius=500)
    
    if circles is not None:
        
            #circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                # circle center
                cv2.circle(poligon, center, 1, (255, 0, 0), 3)
                # circle outline
                radius = i[2]
                cv2.circle(poligon, center, radius, (255, 0, 255), 3)
                print(f"center:{center}, radius:{radius}")   
"""
    cv2.imshow("gray",gray)
    cv2.imshow("poligon",poligon)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return center,radius

poligon=cv2.imread("data\\input\\1.png")

center,radius=radius_finder(poligon)
print(center,radius)

