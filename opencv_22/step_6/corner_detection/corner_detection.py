import numpy as np 
import cv2
import matplotlib.pyplot as plt

chess=cv2.imread("images\\input\\chess.jpg")# foto okundu
chess_board=cv2.imread("images\\input\\chessboard.jpg")
chess_rgb=cv2.cvtColor(chess,cv2.COLOR_BGR2RGB)#renk uzayı rgb formatına çevrildi
chess_board_rgb=cv2.cvtColor(chess_board,cv2.COLOR_BGR2RGB)#renk uzayı rgb formatına çevrildi
plt.imshow(chess)# ekrana bastırılır
plt.waitforbuttonpress()

gray_c=cv2.cvtColor(chess_rgb,cv2.COLOR_RGB2GRAY)#foto gray formata çevrildi
gray_b=cv2.cvtColor(chess_board_rgb,cv2.COLOR_RGB2GRAY)#foto gray formata çevrildi
plt.imshow(gray_c)
plt.waitforbuttonpress()

plt.imshow(chess_board)
plt.waitforbuttonpress()

gray_float=np.float32(gray_c)# fotonun pikselleri float tipine getirildi
# floata çevirme nedeni cornerharris fonksiyonunun float tipinde foto istemesidir
print(gray_float.shape)

#köşe tespiti algoritması
dst=cv2.cornerHarris(gray_float,2,17,0.04)#en sondaki sabit değeri değiştirilebilir ikini

dst=cv2.dilate(dst,None)# erozyon işlemi uygulandı

chess[dst>0.01*dst.max()]=[255,0,0]# harris fonksiyonundan çıkan görüntüden max değerlerinden yüzde bir büyük olan piksellere gerçek resim üzerinde kırmızı ile  boyanır
# ve tespit görüntülenir
plt.imshow(chess)
plt.waitforbuttonpress()

board_float=np.float32(gray_b)#fotonun piksel değerleri floata tipine geldi

dst=cv2.cornerHarris(board_float,2,29,0.04)# köşe tespiti fonksiyonu uyglandı

dst=cv2.dilate(dst,None)# erozyon işlemi uygulandı

chess_board[dst>0.01*dst.max()]=[255,0,0]# harris fonksiyonundan çıkan görüntüden max değerlerinden yüzde bir büyük olan piksellere gerçek resim üzerinde kırmızı ile  boyanır
# ve tespit görüntülenir

plt.imshow(chess_board)
plt.waitforbuttonpress()

# diğer bir algoritma

corners=cv2.goodFeaturesToTrack(gray_b,100,0.01,10)# maxcorner=5 # 3. paramtre en az uzaklık 

corners=np.int0(corners)# integer formatına çevrildi

for i in corners:
    x,y=i.ravel()
    cv2.circle(chess_board_rgb,(x,y),3,(255,0,0),-1)# köşelere çember çizildi

plt.imshow(chess_board_rgb)
plt.waitforbuttonpress()
    










