#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

from pdb import set_trace as st

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
fd = open('../tmp/edf_temp/edfXXX', 'r')

val = fd.read(1)

"""
while(1):
    val = ser.read(1)
    print(val)
    if ord(val) == 2:
        print('=============================')
"""
while 1:
    print('=============================\n')
    frameRaw = []
    frameSTR = ""

    while(ord(val) != 2):
        val = fd.read(1)

    while(ord(val) != 3):
        # print(val)
        # frameRaw.append(val)
        frameSTR += val
        val = fd.read(1)

    frame = frameSTR.split('\n')
    for data in frame:
        if len(data) > 4:
            dataL = data.split(' ') # quand on passera en mode STANDARD, le séparateur sera '\t'
            label = dataL[0]
            value = dataL[1]
            # pour l'instane, on ne s'occupe pas du cheksum
            print("%s %s" % (label, value))

# st()
