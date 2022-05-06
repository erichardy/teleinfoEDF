
from machine import UART
import sys

class dataEDF:

    def __init__():
        pass

    label = ""
    value = ""
    horo = ""
    checksum = ""

out = open('dataFile', "w")

RATE = 9600
# RATE = 1200

# uart = UART(1, baudrate=RATE, tx=33, rx=32, timeout_char=50, txbuf=20)
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
odd = 1
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)

nb = 0
MAX = 3000

while nb < MAX:
    if uart.any() > 0:
        val = uart.read(1)
        # print(val.decode())
        out.write(val)
        # print(val)
        nb += 1

out.close()

print("Fin acquisition")

frameFile = open('frame', "w")
data = open('dataFile', "r")

frame = []
c = data.read(1)
while c != '\x02':
    c = data.read(1)

print("Debut frame")
c = data.read(1)
# sys.exit()
nb = 0
while nb < MAX - 1:
    nb += 1
    if c == '\x03':
        break
    if c != '\x0d':
        frame.append(c)
    c = data.read(1)

data.close()

frameStr = ""

for c in frame:
    frameFile.write(c)
    frameStr += c

frameFile.close()
# print(type(frameStr))
# print(frameStr)
frameList = frameStr.split('\n')
print(frameList)

sys.exit()
labels = {}
values = {}

for d in frameList:
    line = d.split('\t')
    if len(line) > 1:
        de = dataEDF()
        de.label = line[0]
        if len(line) > 3: # 3 champs => donnée horodatee
            de.horo = line[1]
            de.value = line[2]
            de.checksum = line[3]
        else:
            de.value = line[1]
            de.checksum = line[2]






