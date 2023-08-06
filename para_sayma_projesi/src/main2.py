import cv2
import numpy as np
from datetime import datetime

money=cv2.imread("Data\\input\\money.jpg")
roi=money[50:290,100:370]

gri_m=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)



money_b=cv2.medianBlur(gri_m,7)# 2. parametrenin pozitif tek bir sayı olması gerekir


money_circle=cv2.HoughCircles(money_b,cv2.HOUGH_GRADIENT,1,roi.shape[0]/4,param1=200,param2=10,minRadius=30,maxRadius=50)# 4.parametrede çemberler arasındaki azami mesafeyi belirttik bunun için ideal sayıyı yazıldı eğer bozukluklar meyadan gelirse bu sayı ile oynayabilirsin 
# param değerleri metoda özeldir her bu hough metodunda bu param değerlerini koru
#param değerleri ile oyanayabilirsin
# min max radius değerleri ile çemberlerin yarıçap sınırını belirlemiş oluruz

if money_circle is not None:
    count=0
    money_circle=np.uint16(np.around(money_circle))# np around ile cember değerlerini  yuvarlayıp uint 16 formatında aldık
    for i in money_circle[0,:]: #çemberdeki değerler bir bir i ye atılıyor
        cv2.circle(roi,(i[0],i[1]),i[2],(0,255,0),2)
        count=1+count
result="{} coins were counted in the picture".format(count)
print(result)        
now=datetime.now()# dosya katıt için datetime eklendi
time=now.strftime("%A-%H-%M-%S")

cv2.imshow("tespit",money)   
cv2.imwrite("Data\\output\\{}_{}.jpg".format(result,time),money)



cv2.waitKey(0)
cv2.destroyAllWindows()