import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-n","--name",required=True,help="name of the user")# argümanın nasıl yazılması gerektiğini yazdık
args=vars(ap.parse_args())

print("selamlar {} adli kullanici".format(args["name"]))# argümanın nasıl kullanılmasını gerektiğini belirttik
