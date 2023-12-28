import matplotlib.pyplot as plt
import cv2

def plt_imshow(image,title=""):
    try:
        image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    except:
        pass    
    plt.figure()
    plt.imshow(image)
    plt.axis("off")
    plt.title(f"{title}")
    plt.waitforbuttonpress()

def plt_imshow_gray(image,title=""):
    plt.figure()
    plt.imshow(image,cmap="gray")
    plt.axis("off")
    plt.title(f"{title}")
    plt.waitforbuttonpress()
