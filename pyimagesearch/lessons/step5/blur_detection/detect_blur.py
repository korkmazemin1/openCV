from imutils import paths
import argparse
import cv2


def variance_of_laplacian(image):

    return cv2.Laplacian(image,cv2.CV_64F).var()# laplas hesaplanır

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())



    
image = cv2.imread(args["images"])# resim okundu
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)# gray formata çevrildi
fm = variance_of_laplacian(gray)# focus measure bizim resmin blur değeri olarak kabul edilebilir

# burada yapılan işlem aslında laplace ile kenar tespiti işlemine oldukça yakın
# kenarı az tespit edilen bir resimde eğer bizim belirlediğimiz thresh değerinin altında bir değer varsa blurlu olarak kabul ederiz 
# resmin ne kadarına blurlu demek ise bize kalmış
    
text = "Not Blurry"

if fm < args["threshold"]:
    text="Blurry"

cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),	
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
cv2.imshow("Image", image)
	
key = cv2.waitKey(0)
 
    