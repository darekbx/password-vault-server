# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from display_LCD import Display_LCD
from buttons_HW import Buttons_HW
from buttons_HW import HWKey

class MainMenu:

    isDebug = True
    selectedItem = 2
    topItemOffset = 0
    itemsCount = 0
    maxToDisplay = 4
    lcd = None
    buttons = None

    secrets = ["Gmail", "Facebook", "Lego", "Twitter", "Onet", "Flurry", "Atalssian"]

    def init(self):
        self.lcd = Display_LCD(self.isDebug)
        self.lcd.init()

        self.buttons = Buttons_HW(self.isDebug)
        self.buttons.listen_buttons(self.handle_key)

    def display(self):
        image = Image.new("RGB", self.lcd.dimensions(), "WHITE")
        draw = ImageDraw.Draw(image)

        self.itemsCount = len(self.secrets)

        self.display_battery(draw, 100, False)
        self.display_secrets(draw, self.secrets)

        self.lcd.show_image(image)

    def handle_key(self, key):
        if key is HWKey.CENTER:
            item_index = self.topItemOffset + self.selectedItem
            print(self.secrets[item_index])
        elif key is HWKey.UP:
            print(self.topItemOffset)
            if self.topItemOffset > 0:
                self.selectedItem = self.topItemOffset
                self.topItemOffset = max(0, self.topItemOffset - 1)
            else:
                self.selectedItem = max(0, self.selectedItem - 1)

        elif key is HWKey.DOWN:

            max_items = self.maxToDisplay - 1
            if self.selectedItem == max_items and self.itemsCount >= max_items:
                diff = self.itemsCount - max_items - 1
                self.selectedItem = max_items
                self.topItemOffset = min(diff, self.topItemOffset + 1)
            else:
                self.selectedItem = min(self.maxToDisplay, self.selectedItem + 1)
        
        self.display()

    def font_test(self, draw):
        draw.text((14, 12), "Facebook", font = ImageFont.truetype('fonts/nova.ttf', 18), fill = 0)
        draw.text((14, 26), "Facebook", font = ImageFont.truetype('fonts/maki.ttf', 12), fill = 0)

    def display_secrets(self, draw, secrets):
        x = 4
        y = 10
        is_overflow = False
        font = self.provide_font()
        
        for index, secret in enumerate(secrets[self.topItemOffset:(self.topItemOffset + self.maxToDisplay)]):
            if self.selectedItem == index:
                draw.ellipse((5, y + 5, 9, y + 9), fill = 0)
            draw.text((14, y), secret, font = font, fill = 0)
            y += 12

        if self.topItemOffset > 0:
            draw.line((120, 17, 123, 14, 126, 17), fill = 0)

        if (self.selectedItem + self.topItemOffset) is not self.itemsCount - 1:  
            draw.line((120, 57, 123, 61, 126, 57), fill = 0)

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
            draw.line((108, 7, 114, 5, 114, 5, 114, 7, 114, 7, 120, 5), fill = "WHITE", width = 21)

    def provide_font(self, size = 18):
        return ImageFont.truetype('fonts/nova.ttf', size)


m = MainMenu()
m.init()
m.display()
