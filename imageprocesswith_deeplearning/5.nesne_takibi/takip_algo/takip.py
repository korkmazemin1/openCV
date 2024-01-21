"""
-Veri Seti indir+
-resim2video+
-keşifsel_veri analizi
"""
import cv2
import numpy as np 
import matplotlib.pyplot as plt
from os.path import isfile,join
import os 

pathIn =r"img1"
pathOut=r"deneme.mp4"

files =[f for f in os.listdir(pathIn) if isfile(join(pathIn,f))]# path in içinde bulunan resimler for ile alındı

fps=25
size=(1920,1080)# videonun tanımındaki fps ve size

out =cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*"MP4V"),fps,size,True)

for i in files :# videoyu yazdırma
    print(i)
    filename=pathIn+"\\"+i

    img =cv2.imread(filename)
    out.write(img)
out.release()    


