import cv2
import numpy as np

polygon=cv2.imread("data\\input\\1.png")

polygon_gray=cv2.cvtColor(polygon,cv2.COLOR_BGR2GRAY)
polygon_gray=cv2.medianBlur(polygon_gray,5)

ret, thresh1 = cv2.threshold(polygon_gray, 150, 255, cv2.THRESH_BINARY) 

cv2.imshow("thresh",thresh1)
cv2.waitKey(0)
cv2.destroyAllWindows()
