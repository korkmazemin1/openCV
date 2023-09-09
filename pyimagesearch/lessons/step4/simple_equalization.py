import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,help="girilecek resmin yolu")
	
args = vars(ap.parse_args())
"""
histogram eşitlemede temel mantık gray formatta gördüğümüz sert piksel değişimlerini minimize etmek 
bu sayede resmin kontrastını iyileştirip bazı arkada kalmış detayları göz önüne bile getirebiliriz

"""
# komut satırı için kodlar

print("[INFO] loading input image....")
image=cv2.imread(args["image"])# resim okundu
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi

print("[INFO] histogram eşitleniyor... ")
equalized=cv2.equalizeHist(gray)# histogram eşitlemesi yapıldı

cv2.imshow("Input", gray)
cv2.imshow("histogram esitlemesi", equalized)
cv2.waitKey(0)



