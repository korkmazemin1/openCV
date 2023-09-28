from WebcamVideoStream import WebcamVideoStream
#from imutils.video.pivideostream import pivideostream

class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
		framerate=32):
		"""
		if usePiCamera==True:
			a=3
			#from imutils.video.pivideostream import PiVideoStream# eğer rapsperrypi kullanılacak ise kütüphenesi eklenir
			
			#self.stream = PiVideoStream(resolution=resolution,
			#	framerate=framerate)
		"""
		
		self.stream = WebcamVideoStream(src=src)# eğer webcam ise webcam fonksiyonu eklenir
			
	def start(self):
		return self.stream.start()# ilk kare alındı

	def update(self):
		self.stream.update()# bir sonraki kare alındı

	def read(self):		
		return self.stream.read()# kare okundu

	def stop(self):	      	
		self.stream.stop()#işlem bitti