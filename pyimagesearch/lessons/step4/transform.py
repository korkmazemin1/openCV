import numpy as np 
import cv2

def order_points(pts):
    rect=np.zeros((4,2),dtype="float32")

    s=pts.sum(axis=1)# üstsağ-sol, alt sağ-sol noktaları için bellekte  yer ayırdık
    
    rect[0]=pts[np.argmin(s)]# sol üst konum en az x+y toplamına sahip olduğu için min ile bulduk
    rect[2]=pts[np.argmax(s)]# sağ alt ise en fazla x+y toplamına sahip olduğu için max ile bulundu
    
    diff=np.diff(pts,axis=1)# x ve y nin farkını aldık 
    
    rect[1]=pts[np.argmin(diff)]# bu farka göre sağ üst 
    rect[3]=pts[np.argmax(diff)]# ve sol alt noktalar yine aynı mantık ile belirlendi
    
    return rect


def four_point_transform(image,pts):

    rect=order_points(pts)
    (tl,tr,br,bl)=rect # aldığımız noktaları düzenlemek için yazıldı

    widthA=np.sqrt(((br[0]-bl[0])**2)+((br[1]-bl[1])**2))# şeklin konumlarını kuş bakışı şekle getirmek için matematiksel işlemler
    widthB=np.sqrt(((tr[0]-tl[0])**2)+((tr[1]-tl[1])**2))
    maxWidth=max(int(widthA),widthB)


    heightA=np.sqrt(((tr[0]-br[0])**2)+((tr[1]-br[1])**2))
    heightB=np.sqrt(((tl[0]-bl[0])**2)+((tl[1]-bl[1])**2))
    maxHeight=max(int(heightA),int(heightB))

    dst=np.array([
        [0,0],
        [maxWidth-1,0],
        [maxWidth-1,maxHeight-1],
        [0,maxHeight-1]],dtype="float32")
    
    M=cv2.getPerspectiveTransform(rect,dst)# getperspectivetransform fonksiyonu ile başta rect ile aldığımız ve işleme soktuğumuz noktalar kuş bakışı -dst- noktaları ile değişti
    warped=cv2.warpPerspective(image,M,(maxWidth,maxHeight))# warperspective ile kuş bakışı görüntüyü çıkış(output) olarak elde ederiz
    #print("br:",br,"bl:",bl,"tr:",tr,"tl:",tl,"maxWidth",maxWidth,"maxHeight",maxHeight,"widthA",widthA,"widthB",widthB,"heightA",heightA,"heightB",heightB)
    return warped



    