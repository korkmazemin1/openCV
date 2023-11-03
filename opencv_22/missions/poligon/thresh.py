"""
import cv2
import numpy as np
image=cv2.imread("data\\input\\2.png")
def empty(a):
    pass
#we need this for creating trackbar
#track bar fonksiyonu için ihtiyacımz var


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",1000,350)
cv2.createTrackbar("hue min","TrackBars",0,255,empty)
cv2.createTrackbar("hue max","TrackBars",255,255,empty)
cv2.createTrackbar("sat min","TrackBars",0,255,empty)
cv2.createTrackbar("sat max","TrackBars",255,255,empty)
cv2.createTrackbar("val min","TrackBars",0,255,empty)
cv2.createTrackbar("val max","TrackBars",255,255,empty)
#creating track bars
#track bar yapıyoruz 6 adet 3 min 3 max için
while True:
   
    imgHSV =cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #resmi hsv ye çeviriyoruz
    #turning rgb to hsv
    h_min =cv2.getTrackbarPos("hue min","TrackBars")
    h_max =cv2.getTrackbarPos("hue max","TrackBars")
    s_min =cv2.getTrackbarPos("sat min","TrackBars")
    s_max =cv2.getTrackbarPos("sat max","TrackBars")
    v_min =cv2.getTrackbarPos("val min","TrackBars")
    v_max =cv2.getTrackbarPos("val max","TrackBars")
    #trackbardan değeri okyuoruz
    #getting value from trackbar
    print(h_min,h_max,s_min,s_max,v_min,v_max)

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)
    #creating mask
    #maske oluşturuyoruz
    result =cv2.bitwise_and(image,image,mask=mask)
    #resmin üzerine maskeyi eklliyoruz
    #puting mask on img
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    cv2.imshow("img",image)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    """
# bu kod kağan şenkeser hayratıdır
# trackbar kullanarak bulmak istediğimiz rengin hsv kodlarını aldık


import cv2
import numpy as np

point=cv2.imread("data\\input\\2.png")

lower_gray = np.array([0, 0, 127])
upper_gray = np.array([0, 0, 127])

hsv=cv2.cvtColor(point,cv2.COLOR_BGR2HSV)
    
mask1=cv2.inRange(hsv,lower_gray,upper_gray)# 4 adımlı bir mask işlemi uygulandı
cv2.imshow("mask",mask1)
blur=cv2.medianBlur(mask1,5)
blur=cv2.bitwise_not(blur)

contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#kontur bulma fonksiyonu


cv2.drawContours(point,contours,1,(0,0,255),3)
# momnets ile bulunan konturun merkezi hesaplanır
for c in contours:
    M=cv2.moments(c)
    
    cX=int(M["m10"]/ (M["m00"]+ 1e-7))
    cY=int(M["m01"]/(M["m00"]+ 1e-7))
    center=(cX,cY)
print(center)
cv2.circle(point,center,1,(255,0,0))    



cv2.imshow("point",point)
cv2.waitKey(0)
cv2.destroyAllWindows()
