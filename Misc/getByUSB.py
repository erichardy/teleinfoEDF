#!/usr/bin/python3

from pdb import set_trace as st
import serial
from getData import getData, frameToDict

store = open('../tmp/teleinfo', 'w')

ser = serial.Serial('/dev/ttyUSB0', 9600, parity=serial.PARITY_EVEN)
ser.bytesize = serial.SEVENBITS
ser.stopbits = serial.STOPBITS_ONE

MAX = 3
MAX = 50
i = 0

while i < MAX:
    frameBytes = getData(ser)
    labels = frameToDict(frameBytes)
    for label in labels:
        line = label + ':' + labels[label] + '\n'
        store.write(line)
    i += 1





