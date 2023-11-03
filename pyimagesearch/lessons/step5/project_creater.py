import os


proje=input("lütfen oluşturmak istediğin projenin ismini giriniz: ")


os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step5\\{}".format(proje))
open("C:\\openCV\\pyimagesearch\\lessons\\step5\\{}\\main.py".format(proje),"x")
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step5\\{}\\images".format(proje))
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step5\\{}\\images\\input".format(proje))
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step5\\{}\\images\\output".format(proje))

