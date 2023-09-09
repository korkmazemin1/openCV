"""

ALGORİTMA

referansdaki dağilimi kaynağa aktariyoruz
"""
import skimage.exposure as exposure
import matplotlib.pyplot as plt
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=True,help="kaynak resmin yolunu gir")
ap.add_argument("-r", "--reference", required=True,help="referans alınacak resmin yolu")
args = vars(ap.parse_args())

# komut satırı kodları

print("[Info] kaynak ve referans resimleri yükleniyor")
src=cv2.imread(args["source"])
ref=cv2.imread(args["reference"])# referans ve kaynak resimleri yüklendi

print("[INFO] performing histogram matching ... ")
multi=True if src.shape[-1]>1 else False # multi değeri ile çoklu kanal olup olmadığını belirleyip  histogram eşitlemede parametre olarak kullanıyoruz
mathced=exposure.match_histograms(src,ref,multichannel=multi)# histogram eşitlemesi

cv2.imshow("kaynak", src)
cv2.imshow("referans", ref)
cv2.imshow("eslesme",mathced)
cv2.waitKey(0)


(fig,axs)=plt.subplots(norws=3,nclos=3,figsize=(8,8))

for (i,image) in enumerate ((src,ref,mathced)):
     image=cv2.cvtColor(image,cv2.COLORwwwwqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq)

