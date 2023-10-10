import cv2
import numpy as np
import matplotlib.pyplot as plt


full=cv2.imread("images\\input\\image.jpg")# resim yüklendi
part=cv2.imread("images\\input\\template_2.png")



full=cv2.cvtColor(full,cv2.COLOR_BGR2RGB)
plt.imshow(full)
plt.waitforbuttonpress()
part=cv2.cvtColor(part,cv2.COLOR_BGR2RGB)# resimler rgb formatına çevrildi
print(full.shape)# fotonun şeklini yazdırdık

height,width,channels =part.shape# parçanın boyutlarını tek tek aldık

my_method=eval("cv2.TM_CCOEFF")# metodu bir işleme atadık
res =cv2.matchTemplate(full,part,my_method)# template matching fonksiyonu ile parça olan fotomuzun nerede olduğunu ısı haritasından görebiliriz


plt.imshow(res)
plt.waitforbuttonpress()

methods=["cv2.TM_CCOEFF","cv2.TM_CCOEFF_NORMED","cv2.TM_CCORR","cv2.TM_CCORR_NORMED","cv2.TM_SQDIFF","cv2.TM_SQDIFF_NORMED"]# methodları tek tek denemek için bir liste haline getirdik

for x in methods :# methodları for döngüsü ile döndürür
    full_copy=full.copy()
    my_method=eval(x)#my methoda sırası ile kullanabilmek için eval ile atadık
    res=cv2.matchTemplate(full_copy,part,my_method)# methodlar denendi
    

    min_value,max_value,min_loc,max_loc=cv2.minMaxLoc(res)# bu fonksiyon sayesinde eşleşme bölgesine dörtgen çizmek için gerekli değerler alındı
    if x in [cv2.TM_SQDIFF,cv2.TM_SQDIFF_NORMED]:# fonksiyonların farklılıklarına göre konum atamaları belirlendi
        top_left=min_loc
    else:
        top_left=max_loc    
    
    bottom_right=(top_left[0]+width,top_left[1]+height)# sol üst noktasını hesapladığımız tespit dörtgeninin sağ altını hesaplamak adına tespit edilmesi gereken resmin boyutları kullanılmıştır

    cv2.rectangle(full,top_left,bottom_right,(255,0,0),5)# tespit değerleri doğrultusunda dörtgen çizildi
    
    plt.subplot(121)# subplot ile çerçeve üzerinde yan yana durmalarını sağladık
    plt.imshow(res)
    plt.title("detecting")




    plt.subplot(122)
    plt.imshow(full)
    plt.title("template matching")
    plt.suptitle(x)
    plt.waitforbuttonpress()

    


    
