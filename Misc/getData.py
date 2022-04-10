#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

# from pdb import set_trace as st
# from machine import UART

# uart = UART(1, 1200)
# uart.init(1200, bits=1, parity=even, stop=1)

"""
import serial

ser = serial.Serial('/dev/ttyUSB0', 1200, parity=serial.PARITY_EVEN)
ser.bytesize = serial.SEVENBITS
ser.stopbits = serial.STOPBITS_ONE
"""
"""
si on ne peut faire qu'une lecture en binaire sur l'UART, il faudra :
1/ fd = open(......, 'rb')
2/ encoding = 'utf-8'
3/ val = val.decode(encoding)
"""
# fd = open('edfXXX', 'r')
# fd = uart

# val = fd.read(1)

def getData(lab, fd):
    frameSTR = ""
    val = ''

    if fd.any() > 0:
        val = fd.read(1)
    if val:
        while(ord(val) != 2):
            if fd.any() > 0:
                val = fd.read(1)

    if val:
        while(ord(val) != 3):
            frameSTR += val
            if fd.any() > 0:
                val = fd.read(1)

    frame = frameSTR.split('\n')
    for data in frame:
        if len(data) > 4:
            dataL = data.split(' ') # quand on passera en mode STANDARD, le séparateur sera '\t'
            label = dataL[0]
            value = dataL[1]
            # pour l'instane, on ne s'occupe pas du cheksum
            # print("%s %s" % (label, value))
            """
            if label == lab:
                return value
            """
            if value:
                return value
            else:
                return '..XXX..'

# st()
"""
ADCO 391763018216
OPTARIF BBR(
ISOUSC 30
BBRHCJB 001444167
BBRHPJB 002047770
BBRHCJW 000233751
BBRHPJW 000396477
BBRHCJR 000023225
BBRHPJR 000030217
PTEC HPJB
DEMAIN ----
IINST1 000
IINST2 000
IINST3 000
IMAX1 060
IMAX2 060
IMAX3 060
PMAX 05616
PAPP 00349
HHPHC A
MOTDETAT 000000
PPOT 00
"""

