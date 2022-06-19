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

# getFrame : populate the list f[] with chars, 1 frame
def getFrame(uart):
    f = []
    collect()
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
    collect()
    return(f)


# get a list of chars and return 3 dicts : values, horo, checksum
def getDict(f):
    fSTR = ""
    for c in f:
        fSTR += c
    if len(fSTR) != 1159:
        return(None, None, None)
    fList = fSTR.split("\n")
    values = {}
    horos = {}
    checksums = {}
    for field in fList:
        mesure = field.split("\t")
        value = None
        label = mesure[0]
        if len(mesure) == 3:
            value = mesure[1]
            checksum = mesure[2]
            horo = None
        if len(mesure) == 4:
            horo = mesure[1]
            value = mesure[2]
            checksum = mesure[3]
        if value:
            values[label] = value
            horos[label] = horo
            checksums[label] =checksum
    return(values, horos, checksums)

"""
RATE = 9600
# uart = UART(2, baudrate=9600)
# uart.init( baudrate=9600, bits=7, parity=0, stop=1)
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)
enable()
"""

