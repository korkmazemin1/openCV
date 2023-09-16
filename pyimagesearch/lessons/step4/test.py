def midpoint(ptA,ptB):
    return ((ptA[0]+ptB[0])*0.5,(ptA[1]+ptB[1])*0.5)# kordinat düzleminde 2 noktanın orta noktasını hesaplayan fonksiyon

for c in cnts :
    if cv2.contourArea(c)<100:# kontur yeterince büyük değilse görmezden gelinir -küçük parçaları atlamak için-
        continue
    orig=image.copy()
    box=cv2.minAreaRect(c)# bu fonksiyon ile tespit edilen nesnenin etrafını seran en küçük dörtgenin merkezi,eni ,boyu ve dönme açısı bulunur
    box=cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)# dörtgeni çizmek için ise minAreaRect den gelen bilgiler ile köşeler belirlenir
    box=np.array(box,dtype="int")# elde edilen veriler dizi haline gelir

    box=perspective.order_points(box)# noktaları sıralamak için hazırladığımız order_points fonksiyonunu çağırdık
    cv2.drawContours(orig,[box.astype("int")],-1,(0,0,255))# konturlar çizildi

    for (x,y) in box:
        cv2.circle(orig,(int(x),int(y)),5,(0,0,255),-1)# belirlediğimiz renklere ve saptayıp sıraladığımız noktaları sırası ile gereken renklere boyadık

    (tl,tr,br,bl)=box
    (tltrX,tltrY)=midpoint(tl,tr)# üstte sağ ve solun orta noktası
    (blbrX, blbrY) = midpoint(bl, br)#altta sağ be solun orta noktası
    (tlblX, tlblY) = midpoint(tl, bl)# solda üst ve altın orta noktası
    (trbrX, trbrY) = midpoint(tr, br)# sağda üst ve altın orta noktası

    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)# hesapladığımız orta noktalara daire çizildi

    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),(255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),(255, 0, 255), 2)# orta noktaların arasına çizgi çizildi


    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))# üst ve alttaki orta noktaların birbirine olan uzaklığı hesaplandı

    if pixelsPer