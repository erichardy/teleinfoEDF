
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
# from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer
import Courrier_New15
from time import sleep
from time import sleep_ms

from getData import getData

from machine import UART

RATE = 9600
# RATE = 1200

# uart = UART(1, baudrate=RATE, tx=33, rx=32, timeout_char=50, txbuf=20)
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
odd = 1
# uart.init(baudrate=RATE, bits=7, parity=even, stop=1, rxbuf=1)
uart.init(baudrate=RATE, bits=8, parity=None, stop=1)
# print(uart)

# val = uart.read(1)


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

def oledClear():
    oled.fill(0)
    oled.show()

oledDisplay('Init...2')
#@sleep(2)
# oledDisplay(str(uart))
# sleep(2)
# oledDisplay('OK....')
sleep(1)
oledClear()

c = 0
nb = 0
MAX = 400

"""
while nb < MAX:
    # c = uart.write('Coucou\n')
    c = uart.write('t')
    oledDisplay(str(nb))
    if c == 0:
        oledDisplay('Erreur envoi !')
        import sys
        sys.exit(1)
    sleep_ms(10)
    nb += 1

"""
while nb < MAX:
    try:
        if uart.any() > 0:
            val = uart.read(1)
            # val = 1
            if val:
                oledDisplay(str(nb) + ' ' + str(val) + ' ' + val.decode('UTF-8'))
            else:
                oledDisplay('Rien !!!')

        # val = getData(lab, uart)
        # oledDisplay(val)
        sleep_ms(10)
    except:
        oledDisplay('Error !')
    nb += 1

sleep(3)
oledClear()
oledDisplay('End !')

