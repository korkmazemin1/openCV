import cv2
import matplotlib.pyplot as plt 

def sliding_window(image,step,ws):# kaç piksel kayacağını tanımlar -ws dikdörtgen boyutu
    #dikdörtgen boyutuna ve resime göre pencere kayması sağlanır
    for y in range (0, image.shape[0]-ws[1],step):
        for x in range(0,image.shape[1]-ws[0],step):
            # yield ile girilen değer fonksiyonda return edilir ve tekrar çağrılır
            yield(x,y,image[y:y+ws[1],x:x+ws[0]])

image=cv2.imread("husky.webp")
im=sliding_window(image,5,(200,150))

for i , image in  enumerate(im):
    print(i)
    if i ==25000:
        
        plt.imshow(image[2])
        plt.waitforbuttonpress()
