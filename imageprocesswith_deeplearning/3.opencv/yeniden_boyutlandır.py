import cv2

img= cv2.imread("data\\car.jpg")# 0 yazarak gray formatta çektik

print("resim boyutu: ",img.shape)# resmin boyutlarına bakıldı
# gray formatta renk uzayı gözükmez


resized=cv2.resize(img,(800,800))

print("resim boyutu: ",resized.shape)

cropped=img[0:600,0:300]# y üzerinde ilk 400 ve x üzerinde ilk 300 alınır

cv2.imshow("cropped",cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()