# bu kodlar çekilen resmin yolunun yanlış verilmesi durumunda nasıl hata vereceğini göstermesi için yazıldı
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="resmin yolunu yaziniz")
args = vars(ap.parse_args())# resmi yüklemek için komut satırı kodları

image=cv2.imread(args["image"])
(h,w,d)=image.shape
print(f"w:{w},h: {h},d:{d}")# girilen resmin boyutlarını çektik


cv2.imshow("Image",image)
cv2.waitKey(0)