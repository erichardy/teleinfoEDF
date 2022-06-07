"""
gestion de la mémoire : https://micropython.fr/88.lab/optimiser_usage_ram/
les threads en python : https://techtutorialsx.com/2017/10/02/esp32-micropython-creating-a-thread/
"""
import micropython as upy

from machine import UART
from time import sleep
from time import localtime
from time import mktime
# from time import sleep_ms
from  sys import exit
from gc import enable
from gc import collect
from os import remove

# from gc import mem_free
# from gc import mem_alloc


""" OLED """
"""
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

"""
""" END OLED """

f = []
mesures = []
fields = ['DATE', 'SINSTS1', 'SINSTS2', 'SINSTS3']
sinsts = []
cumul = []
MAX_CUMUL = 4

class dataEDF():

    label = ""
    value = ""
    horo = ""
    checksum = ""

# retourne une liste de chars
def getFrame():
    gc.collect()
    f.clear()
    out = open('dataFile', "w")
    nb = 0
    while nb < 3000:
        if uart.any() > 0:
            val = uart.read(1)
            out.write(val)
            nb += 1
    out.close()
    out = open('dataFile', "r")
    c = out.read(1)
    while c != '\x02':
        c = out.read(1)
    nb = 0
    while nb < 2999:
        c = out.read(1)
        if c == '\x03':
            break
        if c != '\x0d':
            f.append(c)
        nb += 1
    out.close()
    remove('dataFile')
    gc.collect()
    return


def getData(frame):
    mesures.clear()
    # convert sequence of bytes to string
    frameSTR = ""
    for c in frame:
        frameSTR += c
    # scan for fields and theire values
    frameList = frameSTR.split('\n')
    for d in frameList:
        line = d.split('\t')
        if len(line) > 1:
            de = dataEDF()
            de.label = line[0]
            # print(":%s:" % (de.label))
            if len(line) > 3: # 3 champs => donnée horodatee
                de.horo = line[1]
                de.value = line[2]
                de.checksum = line[3]
            else:
                de.value = line[1]
                de.checksum = line[2]
                de.horo = ""
            if de.label == 'DATE':
                de.value = de.horo
            if de.label in fields:
                mesures.append(de)
    for m in mesures:
        if m.label == 'DATE':
            date = m.value
        if m.label == 'SINSTS1':
            sinsts1 = m.value
        if m.label == 'SINSTS2':
            sinsts2 = m.value
        if m.label == 'SINSTS3':
            sinsts3 = m.value
    inst = (date, int(sinsts1), int(sinsts2), int(sinsts3))
    sinsts.append(inst)
    if len(cumul) > MAX_CUMUL - 1:
        cumul.pop(0)
    cumul.append(inst)
    gc.collect()
    return

def myData():
    # for t in range(0, MAX_CUMUL + 4):
    for t in range(0, MAX_CUMUL + 5):
        # oledClear()
        # oledDisplay(str(t) + '\n')
        gc.collect()
        # frame = getFrame(uart)
        getFrame()
        l = len(f)
        if l == 1159:
            # oledDisplay(str(l))
            getData(f)
            """
            for m in mesures:
                print("%s:%s:%s:" % (m.label, m.value, m.horo))
            print('\n\n')
            """
        f.clear()
        sleep(5)

def myData2():
    gc.collect()
    getFrame()
    l = len(f)
    if l == 1159:
        getData(f)
    f.clear()


RATE = 9600
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)
gc.enable()

# myData()
while 1:
    myData2()
    lsinsts = len(sinsts)
    if lsinsts > 30:
        break


print(sinsts)
print(cumul)
"""
print(upy.mem_info())
print(mem_free())
print(mem_alloc())
"""

