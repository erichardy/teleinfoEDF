""" OLED """

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
# from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import Courrier_New as Courrier_New15

# ESP32 Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21))
pscl = Pin(22, Pin.OPEN_DRAIN)
psda = Pin(21, Pin.OPEN_DRAIN)
i2c = I2C(scl=pscl, sda=psda)

# OLED
# 2 lignes de 12 caracteres avec la font Courrier_New15
WIDTH = const(128)
HEIGHT = const(32)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
wri = Writer(oled, Courrier_New15)

def oledDisplay(s = 'XXX'):
    Writer.set_textpos(oled, 0, 0)
    wri.printstring(s)
    oled.show()

def oledClear():
    oled.fill(0)
    oled.show()


""" END OLED """
