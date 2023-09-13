"""

ALGORİTMA
1-referans ve kaynak resimleri yükle 
2-resimlerin kanal değerini al
3-match_histogram ile beraber referens ve kaynak resimlerinin histogramlarını eşitle 
4-çıktıları göster
grafikler için
1-3x3 figür oluştur
2-for döngüsü ile 2 boyutlu grafikleri çıktı olarak al

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
#src=cv2.resize(src,(ref.shape[:2]))
print("[INFO] performing histogram matching ... ")
multi=  True if src.shape[-1]>1 else False # multi değeri ile çoklu kanal olup olmadığını belirleyip  histogram eşitlemede parametre olarak kullanıyoruz
mathced=exposure.match_histograms(src,ref,multichannel=multi)# histogram eşitlemesi

cv2.imshow("kaynak", src)
cv2.imshow("referans", ref)
cv2.imshow("eslesme",mathced)
cv2.waitKey(0)


(fig,axs)=plt.subplots(nrows=3,ncols=3,figsize=(8,8))#resimlerin bgr kanallarının histogramını göstermek üzre 3x3 lük bir figür oluşturuldu

for (i,image) in enumerate ((src,ref,mathced)):# --not enumarate fonksiyonu elemanların hem kendisinin hemde indislerinin dönmesini sağlar--
     # bu kısımda i indisleri ve image döngü içerisinde dönecek resimlerin isimlerini döndürür 
     image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)# resim bgr dan rgb ye dönüştürüldü

     for(j,color) in enumerate (("red","green","blue")):# enumarate ile j indisleri color kanal isimlerinş dndürür
           (hist,bins)=exposure.histogram(image[...,j],source_range="dtype")# döngüdeki değerlere göre dönen resmin dönen kanal değeri hesaplanır
           axs[j,i].plot(bins,hist/hist.max())# plot ile beraber bu değer 2 boyutlu fonksiyona çevrilir
           
           (cdf,bins)=exposure.cumulative_distribution(image[...,j])# dönen resmin kanalının kümülatif dağılımı bulunur
           axs[j,i].plot(bins,cdf) # 2 boyutlu grafik haline getirilir

           axs[j,0].set_ylabel(color)# j değerini y eksenine atadık ve color ismini verdik

            # grafikleri göstermek içim gerekli kodlar  ||||||||
axs[0,0].set_title("source")
axs[0, 1].set_title("Reference")
axs[0, 2].set_title("Matched")

plt.tight_layout()
plt.show()