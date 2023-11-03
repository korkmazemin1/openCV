import cv2
import numpy as np 


def radius_finder(poligon):
    
    gray=cv2.cvtColor(poligon,cv2.COLOR_BGR2GRAY)
    
    kernel=np.ones((3,3),np.uint8)
    dilation=cv2.dilate(gray,kernel,iterations=1)
    dilation=cv2.medianBlur(dilation,1)
    cv2.imshow("dilation",dilation)


    rows = gray.shape[0]
    circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=75, param2=200,
                               minRadius=250, maxRadius=1000)
    
    
    """
    gray=cv2.cvtColor(poligon,cv2.COLOR_BGR2GRAY)
    
    kernel=np.ones((3,3),np.uint8)
    dilation=cv2.dilate(gray,kernel,iterations=2)
    th2= cv2.adaptiveThreshold(dilation,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,45,8)
    cv2.imshow("th2",th2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

    
    rows = gray.shape[0]

    circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=100,
                               minRadius=250, maxRadius=1000)

    """
    contours,_=cv2.findContours(th2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#kontur bulma fonksiyonu

    cnt = contours[0]
    (x,y),radius = cv2.minEnclosingCircle(cnt)

    center = (int(x),int(y))
    radius = int(radius)
    cv2.circle(poligon,center,radius,(0,255,0),3)
    cv2.circle(poligon,center,3,(255,255,0),3)
    #print(contours)        

    #cv2.drawContours(poligon,contours,1,(0,0,255),5)

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
    
    #return center,radius

poligon=cv2.imread("data\\input\\1.png")
radius_finder(poligon)
