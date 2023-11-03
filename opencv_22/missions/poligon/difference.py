
def shot_finder():
    img1=cv2.imread("data\\input\\1.png")
    img2=cv2.imread("data\\input\\2.png")

    abs=cv2.absdiff(img1,img2)
    gray_abs=cv2.cvtColor(abs,cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray_abs, 50, 255, cv2.THRESH_BINARY_INV) 
    thresh2 = cv2.adaptiveThreshold(gray_abs, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 199, 5) 

    contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, 
                                cv2.CHAIN_APPROX_SIMPLE) 
    
    # take the first contour 
    i=0
    for c in contours:

            M =cv2.moments(c)
            cX = int(M["m10"] / M["m00"]) 
            cY= int(M["m01"] / M["m00"])

            cv2.drawContours(img2, [c], -1, (0, 255, 0), 2) 
            if i==0:
                    pass
            else:
                print(f"cordinate: {c[0][0]}") 

            i +=1




    cv2.imshow("abs",abs)
    cv2.imshow("gray_abs",gray_abs)
    cv2.imshow("thresh1",thresh1)
    cv2.imshow("thresh2",thresh2)
    cv2.imshow("result",img2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()