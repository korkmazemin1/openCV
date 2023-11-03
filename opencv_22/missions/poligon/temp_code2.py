import cv2

image = cv2.imread('data\\input\\1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    if cv2.contourArea(c) < 10:
        cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

result = 255 - thresh
cv2.imshow('result', result)
cv2.waitKey()