# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from display_LCD import Display_LCD
from buttons_HW import Buttons_HW

class MainMenu:

    isDebug = False
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
        self.display_secrets(draw, ["Gmail", "Facebook", "Lego", "Twitter"])

        self.lcd.show_image(image)

    def handle_key(self, key):
        print(key)

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
        return ImageFont.truetype('Font.ttf', 7)


m = MainMenu()
m.init()
m.display()
