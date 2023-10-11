import os


proje=input("lütfen oluşturmak istediğin projenin ismini giriniz: ")


os.mkdir("C:\\openCV\\opencv_22\\step_7\\{}".format(proje))
open("C:\\openCV\\opencv_22\\step_7\\{}\\{}.py".format(proje,proje),"x")
os.mkdir("C:\\openCV\\opencv_22\\step_7\\{}\\images".format(proje))
os.mkdir("C:\\openCV\\opencv_22\\step_7\\{}\\images\\input".format(proje))
os.mkdir("C:\\openCV\\opencv_22\\step_7\\{}\\images\\output".format(proje))