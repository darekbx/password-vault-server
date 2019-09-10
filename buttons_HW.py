import threading
import time
from enum import Enum

import sys, tty, termios

class HWKey(Enum):
	UP = 0
	DOWN = 1
	CENTER = 2
	LEFT = 3
	RIGHT = 4

class Buttons_HW:

	joystickUp = 6
	joystickDown = 19
	joystickCenter = 13
	joystickLeft = 5
	joystickRight = 26
	callback = None

	_is_debug = False

	def __init__(self, is_debug):
		self._is_debug = is_debug

	def listen_buttons(self, callback):
		self.callback = callback
		if self._is_debug:
			threading.Thread(target = self.debug_keylogger).start()
		else:
			import RPi.GPIO as GPIO
			GPIO.setup(self.joystickUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickCenter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
			GPIO.setup(self.joystickRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
			elif GPIO.input(self.joystickLeft) == False:
				self.handle_key(HWKey.LEFT)
			elif GPIO.input(self.joystickRight) == False:
				self.handle_key(HWKey.RIGHT)
			time.sleep(0.2)

	def handle_key(self, key):
		self.callback(key)

	def debug_keylogger(self):
		lock = threading.Lock()
		while True:
			with lock:
				fd = sys.stdin.fileno()
				old_settings = termios.tcgetattr(fd)
				try:
					tty.setraw(sys.stdin.fileno())
					ch = sys.stdin.read(1)
					if ch is 'w':
						self.handle_key(HWKey.UP)
					elif ch is 's':
						self.handle_key(HWKey.DOWN)
					elif ch is 'c':
						self.handle_key(HWKey.CENTER)
					elif ch is 'a':
						self.handle_key(HWKey.LEFT)
					elif ch is 'd':
						self.handle_key(HWKey.RIGHT)
					else:
						sys.exit()
				finally:
					termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)