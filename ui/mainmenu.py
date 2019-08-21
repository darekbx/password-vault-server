# https://www.waveshare.com/wiki/Libraries_Installation_for_RPi
import LCD_1in44
import LCD_Config

import Image
import ImageDraw
import ImageFont
import ImageColor

class MainMenu:

    def __init__(self):

        LCD = LCD_1in44.LCD()
        
        Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
        LCD.LCD_Init(Lcd_ScanDir)
        
        image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)
        
        draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
        draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
        draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
        draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
        
        draw.rectangle([(18,10),(110,20)],fill = "RED")
        
        draw.text((33, 22), 'WaveShare ', fill = "BLUE")
        draw.text((32, 36), 'Electronic ', fill = "BLUE")
        draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")

        LCD.LCD_ShowImage(image,0,0)

        return

    def display_options(self):
        return