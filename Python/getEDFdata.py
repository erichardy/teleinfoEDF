
# https://docs.python.org/3/library/sqlite3.html

from datetime import datetime
from time import sleep

from manageDates import toDate

from pdb import set_trace as st


def toDate(strDate):
    # strDate is like : "E221019225938"
    #                     123456789012
    y = int(strDate[1:3]) + 2000
    month = int(strDate[3:5])
    d = int(strDate[5:7])
    h = int(strDate[7:9])
    minute = int(strDate[9:11])
    s = int(strDate[11:13])
    theDate = datetime(y, month, d, h, minute, s)
    # print("%s %s %s %s %s %s" % (y, month, d, h, minute, s))
    # we can get separate parameters with datetime object as :
    # theDate.year  theDate.month, etc... with day, hour, minute, second
    return theDate


def reOpenSerial():
    global ser
    ser.close()
    sleep(.5)
    ser = serial.Serial(SERIAL_DEV , 9600, parity=serial.PARITY_EVEN)
    ser.bytesize = serial.SEVENBITS
    ser.stopbits = serial.STOPBITS_ONE


def readSer():
    i = 0
    while i < 20:
        c = ser.read()
        print(c)
        i += 1


def toNum(s):
    if s.isdecimal():
        return int(s)
    return None


def displayN(N):
    nb = 0
    while nb < N:
        f = getOneFrame()
        (val, horos, checksums) = getDict(f)
        DATE = toDate(horos['DATE']).isoformat(' ', timespec='seconds')
        SINSTS1 = val['SINSTS1']
        SINSTS2 = val['SINSTS2']
        SINSTS3 = val['SINSTS3']
        ph1 = toNum(SINSTS1)
        ph2 = toNum(SINSTS2)
        ph3 = toNum(SINSTS3)
        # print("%s %s %s %s" % (DATE, SINSTS1, SINSTS2, SINSTS3))
        print("%s %4i %4i %4i %4i" % (DATE, ph1, ph2, ph3, nb))
        nb += 1


def getNLines(N):
    nb = 0
    while nb < N:
        l = getDataLine()
        print(l)
        nb += 1


