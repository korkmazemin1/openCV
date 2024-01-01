import cv2
import numpy as np 
import matplotlib.pyplot as plt
from imshow import plt_imshow,plt_imshow_gray


image=cv2.imread("data\\team.png",0)

contours,hieararchy=cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)# find contours ile iç ve dış konturlar saptanır(RETR_CCOMP)

external_contours =np.zeros(image.shape)
internal_contours =np.zeros(image.shape)
for i in range (len(contours)):
    if hieararchy[0][i][3]==-1:# bu şartlar sağlandığında external (dışbükey olur)
        cv2.drawContours(external_contours,contours,i,255,-1)# bulunan konturlar external ise external tuvaline çizdirilir
    else:
        cv2.drawContours(internal_contours,contours,i,255,-1)# enternallar ise enternal görseline çizilir
cv2.imshow("external",external_contours)
cv2.imshow("internal",internal_contours)
cv2.waitKey()
cv2.destroyAllWindows()