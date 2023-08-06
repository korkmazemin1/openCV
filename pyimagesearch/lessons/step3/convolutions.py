from skimage.exposure import rescale_intensity
import numpy as np 
import argparse 
import cv2

def convolve(image,kernel):
    (iH,iW)=image.shape[:2]
    (kH,kW)=kernel.shape[:2]# çekirdeğin ve resmin uzamsal boyutlarını aldık 
    pad=(kW-1)//2#çıktı görüntümüzün aynı olması için dolgu(pad) oluşturup kopyaladık

    image=cv2.copyMakeBorder(image,pad,pad,pad,pad,cv2.BORDER_REPLICATE)
    output=np.zeros((iH,iW),dtype="float32")# blurlanmış görüntünün değerlerini almak için sıfırlardan matris oluşturduk- temiz bir palet-

    for y in np.arange(pad,iH+pad):
        for x in np.arange(pad,iW+pad):# kernalin x ve ye kordinatları sağ-sol,yukarı-aşağı hareket edebilmesi için iki tane döngü oluşturduk

            
            roi=image[y-pad:y+pad+1,x-pad:x+pad+1]  #belirlediğimiz roi resim üzerindeki x,y ye göre merkezlenip kernel boyutunu almasını sağladık
            
            k=(roi*kernel).sum()# matrislerdeki elemanlar toplanır ve sonucunda toplamasını alırız
            
            output[y-pad,x-pad]=k # çıktının görüntüsü ayarlandı
        
            output=rescale_intensity(output,in_range=(0,255))
            output=(output*255).astype("uint8")

            return output
        
ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
args=vars(ap.parse_args())# komut satırı ile çalışması için kodlar
        
smallBlur=np.ones((7,7),dtype="float")*(1.0/(7*7))# blur seviyeleri ayarlandı
largeBlur=np.ones((21,21),dtype="float")*(1.0/(21*21))

sharpen=np.array((
            [0, -1, 0],
	        [-1, 5, -1],
	        [0, -1, 0]),dtype="int")# kernel matrisi belirlendi
        # amaca yönelik kerneller mevcut bunlardan hangisine ihtiyaç var ise o kullanılır 

laplacian = np.array((
	        [0, 1, 0],
	        [1, -4, 1],
	        [0, 1, 0]), dtype="int")# laplacian şeklin  kenarlarını saptamak için kullanılır
        
sobelX = np.array((
	        [-1, 0, 1],
	        [-2, 0, 2],
	        [-1, 0, 1]), dtype="int")# sobel fonksiyonları x de ve y de ayrı ayrı çalışarak kenarları saptar
        
sobelY = np.array((
	        [-1, -2, -1],
	        [0, 0, 0],
	        [1, 2, 1]), dtype="int")# 3 kernelde mantık piksel değişimlerinden yararlanmak - grafiklerdeki ani renk(piksel) değişimlerini türevlerini alarak saptadıkdan sonra kenar tespiti yapılıyor.
kernelBank=(
("small_blur",smallBlur),#sözlük halinde sıraladığımız kernelleri for döngüsü ile daha düzenli işleyeceğiz
("large_blur",largeBlur),# bu tür işlemler her ne kadar gereksiz görülsede amatör kodlamadan ayrılmak daha düzenli yapmak için gerekli
("sharpen",sharpen),
("laplacian",laplacian),
("sobel_x",sobelX),
("sobel_y",sobelY)
)

image=cv2.imread(args["image"])
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gri formata çevrildi 

for (kernelName,kernel) in kernelBank:
    print("[INFO] applying {} kernel ".format(kernelName))
    convolveOutput=convolve(gray,kernel)# amaçlarına göre ayarladığımız kernelleri-çekirdekleri- for döngüsü ile sıra ile çekerek gray formata çekilmiş görüntüde uyguluyoruz
    opencvoutput=cv2.filter2D(gray,-1,kernel)

    cv2.imshow("original",gray)
    cv2.imshow("{} - convole".format(kernelName),convolveOutput)
    cv2.imshow("{} - opencv ".format(kernelName),opencvoutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




