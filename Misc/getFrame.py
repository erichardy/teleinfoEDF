"""
gestion de la mémoire : https://micropython.fr/88.lab/optimiser_usage_ram/

les threads en python : https://techtutorialsx.com/2017/10/02/esp32-micropython-creating-a-thread/


"""


from machine import UART
from time import sleep
from time import sleep_ms
from  sys import exit
from gc import enable
from gc import collect
from os import remove

f = []
mesures = []
fields = ['DATE', 'SINSTS1', 'SINSTS2', 'SINSTS3']
SINSTS1 = {}
SINSTS2 = {}
SINSTS3 = {}

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
    frameSTR = ""
    for c in frame:
        frameSTR += c
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
                    break
            for m in mesures:
                if m.label == 'SINSTS1':
                    SINSTS1[date] = m.value
                if m.label == 'SINSTS2':
                    SINSTS2[date] = m.value
                if m.label == 'SINSTS3':
                    SINSTS3[date] = m.value
    gc.collect()
    return

RATE = 9600
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
odd = 1
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)
gc.enable()

for t in range(0, 10):
    gc.collect()
    # frame = getFrame(uart)
    getFrame()
    l = len(f)
    if l == 1159:
        getData(f)
        """
        for m in mesures:
            print("%s:%s:%s:" % (m.label, m.value, m.horo))
        print('\n\n')
        """
    f.clear()
    print(SINSTS1)
    print(SINSTS2)
    print(SINSTS3)
    sleep(1)

