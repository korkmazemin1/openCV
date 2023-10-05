import numpy as np
import cv2
import imutils
def detect(image):
	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
	gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
	gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
	
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)
	
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
	
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	
	closed = cv2.erode(closed, None, iterations=4)
	closed = cv2.dilate(closed, None, iterations=4)
	
	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	
	if len(cnts) == 0:
		return None
	
	c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
	rect = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
	box = np.int0(box)
	
	return box