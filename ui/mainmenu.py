# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

class MainMenu:

    isDebug = True
    LCD = None

    def init_LCD(self):
        if self.isDebug:
            self.LCD = type('Expando', (object,), {})()
            self.LCD.width = 128
            self.LCD.height = 64
            self.LCD.LCD_ShowImage = self.debug_ShowImage
        else:
            import LCD_1in44
            import LCD_Config

            self.LCD = LCD_1in44.LCD()
            Lcd_ScanDir = self.LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
            self.LCD.LCD_Init(Lcd_ScanDir)
    
    def display(self):
        image = Image.new("RGB", (self.LCD.width, self.LCD.height), "BLACK")
        draw = ImageDraw.Draw(image)

        draw.text((33, 22), 'Hello ', fill = "WHITE")

        self.display_battery(draw, 70)

        self.LCD.LCD_ShowImage(image,0,0)

    def display_battery(self, draw, battery_level):
        """
        Parameters
        ----------
        battery_level : int
            Battery level in percent
        """
        color = "RED" if battery_level < 20 else "GREEN"
        value = 16 * (battery_level / 100)
        draw.rectangle([(104, 2), (124, 8)], outline = "WHITE") 
        draw.rectangle([(124, 4), (126, 6)], fill = "WHITE")
        draw.rectangle([(106, 4), (104 + value, 6)], fill = color)

    def debug_ShowImage(self, image, x, y):
        image.show()