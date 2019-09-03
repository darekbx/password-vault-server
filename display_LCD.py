import psutil

class Display_LCD:

	_disp = None
	_is_debug = False

	def __init__(self, is_debug):
		self._is_debug = is_debug

	def init(self):
		if self._is_debug:
			self._disp = type('Expando', (object,), {})()
			self._disp.getbuffer = self.debug_getbuffer
			self._disp.ShowImage = self.debug_ShowImage
			self._disp.width = 128
			self._disp.height = 64
		else:
			import SH1106
			self._disp = SH1106.SH1106()
			self._disp.Init()
			self._disp.clear()

	def dimensions(self):
		return (self._disp.width, self._disp.height)

	def show_image(self, image):
		self._disp.ShowImage(self._disp.getbuffer(image))

	def debug_getbuffer(self, image):
		return image

	def debug_ShowImage(self, image):
		for proc in psutil.process_iter():
			if proc.name() == "display":
				proc.kill()
		image.show()
