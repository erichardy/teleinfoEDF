
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
# from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import Courrier_New15
from time import sleep
from time import sleep_ms

from getData import getData

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

def tryOled():
    Writer.set_textpos(oled, 0, 0)
    wri.printstring('Sunday')
    Writer.set_textpos(oled, 15, 0)
    wri.printstring('1234567890123456789')
    # Writer.set_textpos(oled, 15, 64)
    # wri.printstring('123456789')
    oled.show()

def oledDisplay(s = 'XXX'):
    Writer.set_textpos(oled, 0, 0)
    wri.printstring(s)
    oled.show()

oledDisplay('Init...')
sleep(2)
oledDisplay(str(uart))
sleep(2)
oledDisplay('OK....')
sleep(2)

