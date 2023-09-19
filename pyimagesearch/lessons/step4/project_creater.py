import os
import argparse

proje=input("lütfen oluşturmak istediğin projenin ismini giriniz: ")


os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step4\\{}".format(proje))
open("C:\\openCV\\pyimagesearch\\lessons\\step4\\{}\\main.py".format(proje),"x")
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step4\\{}\\images".format(proje))
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step4\\{}\\images\\input".format(proje))
os.mkdir("C:\\openCV\\pyimagesearch\\lessons\\step4\\{}\\images\\output".format(proje))