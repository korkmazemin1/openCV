# ilk kelimesi aynı olanları ilk kelime ile dosya açıp oraya aktar
import cv2
import pandas as pd 
import numpy as np 
import os
label_list=[]
path_train="data\\fruits-360_dataset\\fruits-360\\Training"
path_test="data\\fruits-360_dataset\\fruits-360\\Test"

def data_process(path,value):
    #veri içerisindeki klasörler listeye alnır
    filelist=os.listdir(path)
    for filename in filelist:
        # her bir verinin ilk kelimesi alınır ve listeye atılır
        label=filename.split(" ")[0]
        # sınıfların sadece ana isimleri alındı
        label_list.append(label)
        # aynı isimli sınıflar teke düştü
    label_list_set=set(label_list)
    #sade etiketli liste döner
   
    for label in label_list_set:
        count=0
        # etikete klasör açılır
        new_path=f"data\\new_{str(value)}\\{label}"
        try:    
            os.makedirs(new_path)
            #ana veri açılır ve içerisindekiler döner
            
            for source in filelist:
                
            
                
                #ilk kelimesi eşleştirilir
                source_split=source.split(" ")[0]
                if source_split==label:
                    #eşleşen klasörde resimler döner3
                    
                    for x in os.listdir(path+"\\"+source):
                        
                        #okunan resim yeni klasöre yazılır
                        img=cv2.imread(path+"\\"+source+"\\"+x)
                        cv2.imwrite(new_path+"\\_"+str(count)+".jpg",img)
                        count=count+1
                else:
                    pass    
        except FileExistsError:
            continue        
        
    


    data_process(path_test,"Test")


