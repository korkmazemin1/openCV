import numpy as np 
import cv2
import matplotlib.pyplot as plt

# grid kafes-kutu anlamına gelir#

chess=cv2.imread("images\\input\\chess.jpg")

isfound,chess_corners=cv2.findChessboardCorners(chess,patternSize=(7,7))# isfound köşe belirleyip belirlemediğini bool olarak verir

print(isfound)

if isfound:
    print("köse bulundu")
else:
    print("köse bulunmadi")

print(chess_corners.shape)  


chess_c=chess.copy()

cv2.drawChessboardCorners(chess_c,(7,7),chess_corners,isfound)# bu chessboard köşe çizim fonksiyonu ile tespit edilen köşeler foto üzerinde çizildi
# ekrana bastırıldı
cv2.imshow("köse",chess_c)
cv2.waitKey(0)
cv2.destroyAllWindows()

dots=cv2.imread("images\\input\\dot_grid.png")# resim okundu

isfound2,circle_grind=cv2.findCirclesGrid(dots,(10,10),cv2.CALIB_CB_SYMMETRIC_GRID)# noktaların gridini bulan fonksiyon # 100 adet noktadan oluştuğu için 10,10 patternsize verdik
# son paramtre bizim fotoğrafımızdaki noktalar simetrik olduğu için verildi farklı görsellerde bu asimetric veya diğerleri ile değişebilir

dots_c=dots.copy()# nokta resminin kopyası

cv2.drawChessboardCorners(dots_c,(10,10),circle_grind,isfound2)# noktaların köşelerini çizmek için yine chessboarda nokta çizen fonksiyondan faydalanıyoruz

cv2.imshow("corner",dots_c)
cv2.waitKey(0)
cv2.destroyAllWindows()






    