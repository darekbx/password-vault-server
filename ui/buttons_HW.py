import threading
import time
from enum import Enum

class HWKey(Enum):
	UP = 0
	DOWN = 1
	CENTER = 2

class Buttons_HW:

	joystickUp = 6
	joystickDown = 19
	joystickCenter = 13
	callback = None

	_is_debug = False

	def __init__(self, is_debug):
		self._is_debug = is_debug

	def listen_buttons(self, callback):
		self.callback = callback
		if self._is_debug:
			self.handle_key(HWKey.CENTER)
		else:
			import RPi.GPIO as GPIO
			GPIO.setup(self.joystickUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickCenter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			threading.Thread(target=self.buttons_worker).start()

	def buttons_worker(self):
		import RPi.GPIO as GPIO
		while True:
			if GPIO.input(self.joystickUp) == False:
				self.handle_key(HWKey.UP)
			elif GPIO.input(self.joystickDown) == False:
				self.handle_key(HWKey.DOWN)
			elif GPIO.input(self.joystickCenter) == False:
				self.handle_key(HWKey.CENTER)
			time.sleep(0.2)

	def handle_key(self, key):
		self.callback(key)
