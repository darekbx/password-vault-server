# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from enum import Enum
import time

from display_LCD import Display_LCD
from buttons_HW import Buttons_HW
from buttons_HW import HWKey

class MainMenu:

    class MenuMode(Enum):
        SECRETS = 0
        SECRET = 1
        OPTIONS = 2

    isDebug = True
    selectedItem = 0
    topItemOffset = 0
    itemsCount = 0
    maxToDisplay = 4
    lcd = None
    buttons = None

    backItem = "[BACK]"
    mode = MenuMode.OPTIONS

    secretsCallback = None

    def init(self):
        self.lcd = Display_LCD(self.isDebug)
        self.lcd.init()

        self.buttons = Buttons_HW(self.isDebug)
        self.buttons.listen_buttons(self.handle_key)

    def display(self):
        image = Image.new("RGB", self.lcd.dimensions(), "WHITE")
        draw = ImageDraw.Draw(image)

        self.display_battery(draw, 100, False)

        if self.mode is self.MenuMode.SECRETS:
            secrets = self.secretsCallback()
            if len(secrets) > 0:
                secrets.insert(len(secrets), self.backItem)
            self.display_secrets(draw, secrets)
        elif self.mode is self.MenuMode.SECRET:
            ""
        elif self.mode is self.MenuMode.OPTIONS:
            self.display_options(draw)

        self.lcd.show_image(image)

    def handle_key(self, key):
        if key is HWKey.CENTER:
            self.hande_key_center()
        elif key is HWKey.UP:
            self.handle_key_up()
        elif key is HWKey.DOWN:
            self.handle_key_down()
        self.display()

    def hande_key_center(self):
        if self.mode == self.MenuMode.OPTIONS:
            self.change_mode(self.MenuMode.SECRETS)
        elif self.mode == self.MenuMode.SECRETS:
            item_index = self.topItemOffset + self.selectedItem
            if self.itemsCount == 0 or item_index == self.itemsCount - 1:
                self.change_mode(self.MenuMode.OPTIONS)

    def handle_key_up(self):
        if self.topItemOffset > 0:
            self.selectedItem = self.topItemOffset
            self.topItemOffset = max(0, self.topItemOffset - 1)
        else:
            self.selectedItem = max(0, self.selectedItem - 1)

    def handle_key_down(self):
        max_items = self.maxToDisplay - 1
        if self.selectedItem == max_items and self.itemsCount >= max_items:
            diff = self.itemsCount - max_items - 1
            self.selectedItem = max_items
            self.topItemOffset = min(diff, self.topItemOffset + 1)
        else:
            max_position = min(self.itemsCount - 1, self.maxToDisplay)
            self.selectedItem = min(max_position, self.selectedItem + 1)

    def change_mode(self, mode):
        self.topItemOffset = 0
        self.selectedItem = 0
        self.mode = mode

    def display_options(self, draw):
        self.display_list(draw, ["Secrets", "Add"])

    def display_secret(self, draw):
        return

    def display_secrets(self, draw, secrets):
        self.display_list(draw, secrets)

    def display_list(self, draw, items):
        y = 10
        font = self.provide_font()
        self.itemsCount = len(items)
        
        print(self.itemsCount)
        if self.itemsCount == 0:
            draw.text((40, 25), "Empty list", font = font, fill = 0)
            return

        for index, item in enumerate(items[self.topItemOffset:(self.topItemOffset + self.maxToDisplay)]):
            if self.selectedItem == index:
                draw.ellipse((5, y + 5, 9, y + 9), fill = 0)
            draw.text((14, y), item, font = font, fill = 0)
            y += 12

        if self.itemsCount > self.maxToDisplay:
            if self.topItemOffset > 0:
                draw.line((120, 18, 123, 13, 126, 18), fill = 0)

            if (self.selectedItem + self.topItemOffset) is not self.itemsCount - 1:  
                draw.line((120, 57, 123, 62, 126, 57), fill = 0)

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
        path = 'fonts/nova.ttf' if self.isDebug else '/home/pi/password-vault-server/ui/fonts/nova.ttf'
        return ImageFont.truetype(path, size)