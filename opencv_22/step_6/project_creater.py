import os


proje=input("lütfen oluşturmak istediğin projenin ismini giriniz: ")


os.mkdir("C:\\openCV\\opencv_22\\step_6\\{}".format(proje))
open("C:\\openCV\\opencv_22\\step_6\\{}\\{}.py".format(proje,proje),"x")
os.mkdir("C:\\openCV\\opencv_22\\step_6\\{}\\images".format(proje))
os.mkdir("C:\\openCV\\opencv_22\\step_6\\{}\\images\\input".format(proje))
os.mkdir("C:\\openCV\\opencv_22\\step_6\\{}\\images\\output".format(proje))