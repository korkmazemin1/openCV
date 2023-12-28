import cv2
import numpy as np

kart=cv2.imread("data\\card.png")# resim okundu

width= 400
height=500# nihai resmin boyutları

pts1=np.float32([[223,3],[83,329],[456,105],[315,428]])# yamuk olan ilk fotodaki kartın köşe kordinatları
pts2=np.float32([[0,0],[0,height],[width,0],[width,height]])# düzeltme sonucu köşe kordinatları

matrix=cv2.getPerspectiveTransform(pts1,pts2)# eski ve yeni kordinatlrı verilen kart perspektif yöntemi ile düzeltecek matris

print(matrix)

output=cv2.warpPerspective(kart,matrix,(width,height))# konum matrisleri ve boyutu belirlenen resmin perpektifi yeniden ayarlandı

cv2.imshow("yeni_kart",output)
cv2.waitKey(0)
