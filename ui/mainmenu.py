# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from display_LCD import Display_LCD
from buttons_HW import Buttons_HW

class MainMenu:

    isDebug = True
    selectedItem = 2
    lcd = None
    buttons = None

    def init(self):
        self.lcd = Display_LCD(self.isDebug)
        self.lcd.init()

        self.buttons = Buttons_HW(self.isDebug)
        self.buttons.listen_buttons(self.handle_key)

    def display(self):
        image = Image.new("RGB", self.lcd.dimensions(), "WHITE")
        draw = ImageDraw.Draw(image)

        self.display_battery(draw, 100, False)
        #self.display_secrets(draw, ["Gmail", "Facebook", "Lego", "Twitter"])
        self.font_test(draw)

        self.lcd.show_image(image)

    def handle_key(self, key):
        print(key)

    def font_test(self, draw):
        draw.text((14, 0), "Facebook", font = ImageFont.truetype('fonts/game.ttf', 22), fill = 0)
        draw.text((14, 12), "Facebook", font = ImageFont.truetype('fonts/mono.ttf', 12), fill = 0)
        draw.text((14, 26), "Facebook", font = ImageFont.truetype('fonts/smash.ttf', 10), fill = 0)
        draw.text((14, 32), "Facebook", font = ImageFont.truetype('fonts/wave.ttf', 14), fill = 0)
        draw.text((14, 44), "Facebook", font = ImageFont.truetype('fonts/apple.ttf', 10), fill = 0)
        draw.text((14, 52), "Facebook", font = ImageFont.truetype('fonts/pixel.ttf', 10), fill = 0)

    def display_secrets(self, draw, secrets):
        x = 4
        y = 12
        font = self.provide_font()
        for index, secret in enumerate(secrets):
            if self.selectedItem == index:
                draw.ellipse((5, y + 5, 9, y + 9), fill = 0)
            draw.text((14, y), secret, font = font, fill = 0)
            y += 12

    def display_battery(self, draw, battery_level, is_charging=False):
        """
        Parameters
        ----------
        battery_level : int
            Battery level in percent
        """
        value = 18 * (battery_level / 100)
        draw.rectangle([(104, 2), (124, 10)], outline = 0) 
        draw.rectangle([(124, 6), (126, 8)], fill = 0)
        draw.rectangle([(106, 4), (104 + value, 8)], fill = 0)

        if is_charging:
            draw.line((108, 7, 114, 5, 114, 5, 114, 7, 114, 7, 120, 5), fill = "WHITE")

    def provide_font(self):
        return ImageFont.truetype('fonts/Font.ttf', 18)


m = MainMenu()
m.init()
m.display()
