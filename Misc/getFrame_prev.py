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

f = []
mesures = []
fields = ['DATE', 'SINSTS1', 'SINSTS2', 'SINSTS3', 'SMAXSN1', 'SMAXSN2', 'SMAXSN3']
fields_SMAXSN = ['SMAXSN1', 'SMAXSN2', 'SMAXSN3']
sinsts = []
cumul = []
MAX_CUMUL = 4

class dataEDF():
    label = ""
    value = ""
    horo = ""
    checksum = ""

# getFrame : populate the list f[] with chars, 1 frame
def getFrame():
    f = []
    gc.collect()
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
    return(f)


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


RATE = 9600
# uart = UART(2, baudrate=9600)
# uart.init( baudrate=9600, bits=7, parity=0, stop=1)
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)
gc.enable()

f = getFrame()
# print(getDict(f))
(v, h, c) = getDict(f)
if v:
    for k in v.keys():
        print("%s_:_%s" % (k, v[k]))

"""
# myData()
while 1:
    myData2()
    lsinsts = len(sinsts)
    if lsinsts > 3:
        break


print(sinsts)
print(cumul)
"""
"""
print(upy.mem_info())
print(mem_free())
print(mem_alloc())
"""

