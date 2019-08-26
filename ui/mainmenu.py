# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

class MainMenu:

    isDebug = False
    disp = None
    selectedItem = 2

    def init_LCD(self):
        if self.isDebug:
            self.disp = type('Expando', (object,), {})()
            self.disp.width = 128
            self.disp.height = 64
            #self.disp.ShowImage(disp.getbuffer = self.debug_ShowImage
        else:
            import SH1106

            self.disp = SH1106.SH1106()
            self.disp.Init()
            self.disp.clear()
    
    def display(self):
        image = Image.new("RGB", (self.disp.width, self.disp.height), "BLACK")
        draw = ImageDraw.Draw(image)

        self.display_battery(draw, 100, True)
        self.display_secrets(draw, ["Gmail", "Facebook", "Lego", "Twitter"])

        self.disp.ShowImage(self.disp.getbuffer(image))

    def display_secrets(self, draw, secrets):
        x = 4
        y = 12
        fnt = ImageFont.truetype('Font.ttf', 12)
        for index, secret in enumerate(secrets):
            if self.selectedItem == index:
                draw.ellipse((5, y + 5, 9, y + 9), fill = (70,130,180))
            draw.text((14, y), secret, font = fnt, fill = "WHITE")
            y += 12

    def display_battery(self, draw, battery_level, is_charging=False):
        """
        Parameters
        ----------
        battery_level : int
            Battery level in percent
        """
        color = "RED" if battery_level < 20 else "GREEN"
        value = 18 * (battery_level / 100)
        draw.rectangle([(104, 2), (124, 10)], outline = "WHITE") 
        draw.rectangle([(124, 6), (126, 8)], fill = "WHITE")
        draw.rectangle([(106, 4), (104 + value, 8)], fill = color)

        if is_charging:
            draw.line((108, 7, 114, 5, 114, 5, 114, 7, 114, 7, 120, 5), fill = "WHITE")

    def debug_ShowImage(self, image, x, y):
        image.show()

m = MainMenu()
m.init_LCD()
m.display()