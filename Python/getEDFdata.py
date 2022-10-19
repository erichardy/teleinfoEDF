#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
# must adapt shebang above !

# from pySerial package
import serial
from pdb import set_trace as st

SERIAL_DEV = '/dev/ttyUSB0'
SERIAL_DEV = '/dev/tty.usbserial-A50285BI'

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
        print(d)


st()

f = getOneFrame()
st()
(val, horos, checksums) = getDict(f)

st()


