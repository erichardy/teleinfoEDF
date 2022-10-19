#!/usr/bin/python3
# must adapt shebang above !

# from pySerial package
import serial
from datetime import datetime

from pdb import set_trace as st

SERIAL_DEV = '/dev/ttyUSB0'

ser = serial.Serial(SERIAL_DEV , 9600, parity=serial.PARITY_EVEN)
ser.bytesize = serial.SEVENBITS
ser.stopbits = serial.STOPBITS_ONE


def getOneFrame():
    frame = []
    val = ser.read(1)
    while(val != b'\x02'):
        val = ser.read(1)

    while(val != b'\x03'):
        # print(val)
        val = ser.read(1)
        frame.append(val)
    return frame

# get a list of chars and return 3 dicts : values, horo, checksum
def getDict(f):
    fSTR = ""
    for c in f:
        fSTR += c.decode('utf-8')
    if len(fSTR) != 1213:
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
            if label == 'DATE':
                value = 'x'     # correction du bug dans la trame emise
            checksum = mesure[3]
        if value:
            values[label] = value
            horos[label] = horo
            checksums[label] =checksum
    return(values, horos, checksums)

def readSer():
    i = 0
    while i < 20:
        c = ser.read()
        print(c)
        i += 1


def toDate(strDate):
    # strDate is like : "E221019225938"
    #                     123456789012
    y = int(strDate[1:3])
    m = int(strDate[3:5])
    d = int(strDate[5:7])
    h = int(strDate[7:9])
    m = int(strDate[9:11])
    s = int(strDate[11:13])
    theDate = datetime(y, m, d, h, m, s)
    # we can get separate parameters with datetime object as :
    # theDate.year  theDate.month, etc... with day, hour, minute, second
    return theDate


def toNum(s):
    if s.isdecimal():
        return int(s)
    return None

# f = getOneFrame()
# (val, horos, checksums) = getDict(f)
nb = 0
while nb < 2000:
    f = getOneFrame()
    (val, horos, checksums) = getDict(f)
    DATE = horos['DATE']
    SINSTS1 = val['SINSTS1']
    SINSTS2 = val['SINSTS2']
    SINSTS3 = val['SINSTS3']
    ph1 = toNum(SINSTS1)
    ph2 = toNum(SINSTS2)
    ph3 = toNum(SINSTS3)

    # print("%s %s %s %s" % (DATE, SINSTS1, SINSTS2, SINSTS3))
    print("%s %4i %4i %4i %4i" % (DATE, ph1, ph2, ph3, nb))
    
    nb += 1


