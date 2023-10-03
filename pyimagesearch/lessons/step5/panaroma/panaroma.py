import numpy as np
import imutils
import cv2


class Stitcher:
    def __init__ (self):
        self.isv3=imutils.is_cv3(or_better=True)# opencv versiyon kontrolü
    
    def stitch(self,images,ratio=0.75,reprojThresh=4.0,showMatches=False):# image parametresi iki resmin dizi hali# reprojthresh ise RANSAC algoritmasındaki esneklik payı

        (imageB,imageA)=images# iki resmi ayırdık
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)# her iki resim için yerel değişmezler ve keypointler tanımlandı

        M = self.matchKeypoints(kpsA, kpsB,featuresA, featuresB, ratio, reprojThresh)# iki resimin verilerini eşleştirdik
        
        if M is None :#eşleşme yok ise None döner
            return None
        
        (matches,H,status)=M# ransac için  H Homography matrix,status ise ransac ile eşleşen noktaların kordinatları
        result=cv2.warpPerspective(imageA,H,(imageA.shape[1] + imageB.shape[1], imageA.shape[0]))# panaroma yapacağımız için genişlikleri toplarız
        result[imageB.shape[0],0:imageB.shape[1]]=imageB


        if showMatches:
            vis =self.drawMatches(imageA,imageB,kpsA,kpsB,matches,status)# eşleşmeleri gösteririz

            return(result,vis)# panaromanın sonucunu ve eşleşme görselleştirmesi döner
        return(result)    
    
    def detectAndDescribe(self,image):
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)# resim gray formata çevrildi

        if self.isv3:# opencv sürüm kontrolü
            descriptor=cv2.xfeatures2d.SIFT_create()# DoG anahtar noktalarını ve SIFT özelliklerini örnekler
            (kps,features)= descriptor.detectAndCompute(image,None)# anahtar noktalarının ve özelliklerinin çıkarılmasını yönetir

        else:# aynı işlemleri opncv 2.4 versiyonları için yapar
            detector=cv2.FastFeatureDetector_create("SIFT")    
            kps = detector.detect(gray)

            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
        
        kps=np.float32([kp.pt for kp in kps])# keypointler dizi haline getirildi

        return (kps,features)    
    
    def matchKeypoints(self,kpsA,kpsB,featuresA,featuresB,ratio,reprojThresh):
        matcher=cv2.DescriptorMatcher_create("BruteForce")# her iki görüntüde öklid mesafesi hesaplanır ve en az olanlar alınır
        rawMatches = matcher.knnMatch(featuresA,featuresB,2)# özellik vektörlerinin  her birinden en iyi iki eşleşmeyi alır
        matches=[]
        
        for m in rawMatches:# false-positive den kaçınmak için bütün eşleşmeleri döngüye soktuk

            if len(m)==2 and m[0].distance<m[1]*ratio:# mesafeleri LOWE oranı testine sokarak teker teker teker kontrol ettik
                matches.append((m[0].trainIdx,m[0].queryIdx))

        if len(matches) > 4:# homografiyi hesaplamak için 4 den fazla eşleşme ararız
            ptsA =np.float32([kpsA[i] for (_,i)in matches])        
            ptsB = np.float32([kpsB[i] for (i, _) in matches])    

            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,reprojThresh)# homografi bulundu

            return(matches,H,status)
        
        return None
    
    def drawMatches(self,imageA,imageB,kpsA,kpsB,matches,status):
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB



        for ((trainIdx, queryIdx), s) in zip(matches, status):
			# keypointler tamamsa işleme başlar
            if s==1:
                ptA=(int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB=(int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis,ptA,ptB,(0,255,0),1) 
        
        return vis          