from PIL import ImageFont

from buttons_HW import HWKey
import debug

class SaltSelect:

	salt = [0, 0, 0, 0]
	active_segment = 0
	saltCallback = None

	def handleKey(self, key):
		if key is HWKey.CENTER:
			self.hande_key_center()
		elif key is HWKey.UP:
			self.handle_key_up()
		elif key is HWKey.DOWN:
			self.handle_key_down()
		if key is HWKey.LEFT:
			self.handle_key_left()
		elif key is HWKey.RIGHT:
			self.handle_key_right()

	def hande_key_center(self):
		result = self.saltCallback("".join(map(str, self.salt)))
		if not result:
			self.active_segment = 0

	def handle_key_up(self):
		if self.active_segment < 4:
			value = self.salt[self.active_segment]
			if value >= 9:
				value = -1
			self.salt[self.active_segment] = value + 1

	def handle_key_down(self):
		if self.active_segment < 4:
			value = self.salt[self.active_segment]
			if value <= 0:
				value = 10
			self.salt[self.active_segment] = value - 1

	def handle_key_left(self):
		if self.active_segment > 0:
			self.active_segment = self.active_segment - 1

	def handle_key_right(self):
		if self.active_segment < len(self.salt):
			self.active_segment = self.active_segment + 1
	
	def display(self, draw):

		start_offset = 10
		for i in range(1, 5):
			x_position = i * 20 + start_offset
			if self.active_segment == i - 1:
				draw.rectangle([(x_position - 2, 24), (x_position + 8, 41)], fill = 0)
				self.draw_segment(draw, i - 1, x_position, (255, 255, 255))
			else:
				self.draw_segment(draw, i - 1, x_position)

		if self.active_segment == 4:
			draw.rectangle([(110 - 2, 24), (110 + 8, 41)], fill = 0)
			self.draw_arrow_right(draw, 110, 28, (255, 255, 255))
		else:
			self.draw_arrow_right(draw, 110, 28)

	def draw_segment(self, draw, index, x, color = 0):
		font = self.provide_font()
		self.draw_arrow_up(draw, x, 14)
		self.draw_arrow_down(draw, x, 46)
		draw.text((x, 20), "{0}".format(self.salt[index]), font = font, fill = color)

	def draw_arrow_up(self, draw, x, y):
		draw.polygon([(0 + x, 5 + y), (3 + x, 0 + y), (6 + x, 5 + y)], fill = 0)

	def draw_arrow_down(self, draw, x, y):
		draw.polygon([(0 + x, 0 + y), (3 + x, 5 + y), (6 + x, 0 + y)], fill = 0)

	def draw_arrow_right(self, draw, x, y, color = 0):
		draw.polygon([(0 + x, 0 + y), (5 + x, 5 + y), (x, 10 + y)], fill = color)

	def provide_font(self, size = 28):
		path = 'fonts/nova.ttf' if debug.isDebug() else '/home/pi/password-vault-server/fonts/nova.ttf'
		return ImageFont.truetype(path, size)
