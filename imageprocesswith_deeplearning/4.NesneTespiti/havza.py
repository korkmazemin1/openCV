import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Resmi oku
img = cv.imread('data\\watershed_coins.webp')
assert img is not None, "Dosya okunamadı, os.path.exists() ile kontrol edin"

# Gri tonlamaya dönüştür
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

# Gürültüyü temizleme
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)

# arka_plan
sure_bg = cv.dilate(opening, kernel, iterations=3)
# ön plan
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)# iki resimin farkı çıkarılır
ret, markers = cv.connectedComponents(sure_fg)
#birbirine bağlı nesneleri bulur ve etiket atar
markers = markers + 1
#
markers[unknown == 255] = 0

# Watershed algoritması uygula
markers = cv.watershed(img, markers)

# Watershed sonucunda -1 olan alanları kırmızıya boyala
img[markers == -1] = [255, 0, 0]

ter
cv.imshow("Sonuc", img)
cv.waitKey()
