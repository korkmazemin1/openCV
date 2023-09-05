from transform import four_point_transform
import transform 
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
ap.add_argument("-c", "--coords",# burada noktaları  girdik
	help = "noktalarin virgül ile ayrilmiş listesi")
args = vars(ap.parse_args())





image = cv2.imread(args["image"])
pts = np.array(eval(args["coords"]), dtype = "float32")


warped = four_point_transform(image, pts)

cv2.imshow("Original", image)
cv2.imshow("Warped", warped)
cv2.waitKey(0)