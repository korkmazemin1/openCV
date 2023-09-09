import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,help="yolu girilecek resim")
ap.add_argument("-c", "--clip", type=float, default=2.0,help="thresholdun kontrast limiti")
ap.add_argument("-t", "--tile", type=int, default=8,help="ızgara boyutu- tile grid")
args = vars(ap.parse_args())

# komut satırı kodları

print("[INFO] resim içe aktarılıyor...")
image=cv2.imread(args["image"])# resim yüklendi
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# gray formata çevrildi

print("[INFO]  CLAHE yapılıyor...")
clahe=cv2.createCLAHE(clipLimit=args["clip"],tileGridSize=(args["tile"],args["tile"]))# adaptive histogram yapıldı clip parametresi kontrast seviyesini belirleken
# tile size ise histogram eşitlenirken resim ızgaralara bölünür 2x2 gibi bunu biz belirler ve optime ızgara büyüklüğünü yazarız
equalized=clahe.apply(gray)# eşitleme gray üzerine uygulandı

cv2.imshow("input",gray)
cv2.imshow("CLAHE",equalized)
cv2.waitKey(0)
cv2.destrolAllWindows()