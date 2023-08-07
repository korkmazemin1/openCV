import cv2
import imutils
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path to input image")
args = vars(ap.parse_args())
#^^^^komut satırı için gereken kodlar^^^^^^^

image=cv2.imread(args["image"])
cv2.imshow("image",image)
cv2.waitKey(0)