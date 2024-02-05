#CNN mimarisinde kullanılan piramit yöntemi
import cv2
import matplotlib.pyplot as plt

def image_pyramid(image,scale=1.5,minSize=(10,10)):

    yield image

    while True:
        #yeniden boyutlandırma
        w = int(image.shape[1]/scale)
        
        image= cv2.resize(image,dsize=(w,w))
        # belirtilen minsize a gelene kadar bölünmeye devam eder
        if image.shape[0]<minSize[1] or image.shape[1] < minSize[0]:
            break
        yield image    


image=cv2.imread("husky.webp")

im=image_pyramid(image)
for  i,image in enumerate(im):
    # bölünen 8.görseli göster
    print(i)
    if i==8:
        plt.imshow(image)
        plt.waitforbuttonpress()