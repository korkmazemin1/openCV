import cv2
import numpy as np 
from imshow import plt_imshow,plt_imshow_gray
import matplotlib.pyplot as plt

img=cv2.imread("data\\red_blue.png")
img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)# renk uzayı değiştirildi

print(img.shape)

img_histogram=cv2.calcHist([img],channels=[0],mask=None,histSize=[256],ranges=[0,256]) # channelı sıfır yapmamızın sebebi gray oluşu--- burada histogram yani renk değerlerinin dağılımı bulundu
print(img_histogram.shape)# burada tek kanal bulunur
plt.figure()
plt.plot(img_histogram)
plt.waitforbuttonpress()

color={"b","g","r"}
plt.figure()
for i,c in enumerate(color):# kanal isimlerini numarlandırır
    histogram=cv2.calcHist([img],channels=[i],mask=None,histSize=[256],ranges=[0,256]) # ile channelları numaralandırdık
    plt.plot(histogram,color=c)
    plt.waitforbuttonpress()
    
   

golden_gate=cv2.imread("data\\golden_gate(1).jpg")
golden_gate_vis=cv2.cvtColor(golden_gate,cv2.COLOR_BGR2RGB)


mask=np.zeros(golden_gate.shape[:2],np.uint8)
plt_imshow(mask)
print(golden_gate.shape)
mask[500:800,100:400]=255
plt_imshow_gray(mask)

masked_img_vis=cv2.bitwise_and(golden_gate_vis,golden_gate_vis,mask=mask)
masked_img_vis=cv2.cvtColor(masked_img_vis,cv2.COLOR_BGR2RGB)

plt_imshow(masked_img_vis)
masked_img_histogram=cv2.calcHist([masked_img_vis],channels=[1],mask=mask,histSize=[256],ranges=[0,256]) # ile channelları numaralandırdık

plt.plot(masked_img_histogram)
plt.waitforbuttonpress()

golden_gate=cv2.imread("data\\paper.jpg",0)
golden_gate_vis=cv2.cvtColor(golden_gate,cv2.COLOR_BGR2RGB)
mask=np.zeros(golden_gate.shape[:2],np.uint8)

mask[500:800,100:400]=255
img_hist=cv2.calcHist([golden_gate],channels=[0],mask=None,histSize=[256],ranges=[0,256]) # calchist ile resmin kanal değerlerine göre histogram değerleri hesaplandı

plt_imshow(golden_gate)
plt.figure() 
plt.plot(img_hist)
plt.waitforbuttonpress()


eq_hist=cv2.equalizeHist(golden_gate)# histogram eşitlemenin sadece grayscale resimlerle çalış
plt_imshow_gray(eq_hist)
img_hist=cv2.calcHist([eq_hist],channels=[0],mask=None,histSize=[256],ranges=[0,256]) # calchist ile resmin kanal değerlerine göre histogram değerleri hesaplandı

plt_imshow(golden_gate)
plt.figure() 
plt.plot(img_hist)
plt.waitforbuttonpress()