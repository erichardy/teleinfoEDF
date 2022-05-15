"""
Capture d'une trame de données :
1- pour être certains de capturer une trame complète, on capte 3000 caractères
2- ces 3000 caractères on les stocke dans un fichier : dataFile (**1**)
3- (**2**) on lit le fichier et on ne capte qu'une trame, c'est-à-dire à partir
  du caratère STX (\x02), on mey tout ça dans une liste de caractères : frame[]
4- (**3**) on remet tous ces caractères dans une STR (frameSTR) pour utiliser
  par la suite la méthode split()
5- (**4**) on isole les données, chaque donnée par split('\n')
6- on met ensuite toutes ces données dans des objets de classe dataEDF
  par la méthode split('\t') qui permet d'isoler les labels et les champs

"""
from machine import UART
from time import sleep_ms
import sys

class dataEDF():

    label = ""
    value = ""
    horo = ""
    checksum = ""

# RATE = 1200
# uart = UART(1, baudrate=RATE, tx=33, rx=32, timeout_char=50, txbuf=20)
RATE = 9600
uart = UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
odd = 1
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)
# (**1**)
nb = 0
MAX = 3000
TRIES = 10
t = 0
READS = False

out = open('dataFile', "w")
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

"""
data = open('dataFile', "r")
nbFrames = 1
nbChars = 1
while 1:
    c = data.read(1)
    if not c:
        break
    nbChars += 1
    if c == '\x02':
        print("nb frames : %i   nb chars : %i" % (nbFrames, nbChars))
        nbFrames += 1
        nbChars = 0
data.close()
"""
# (**2**)
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

# (**3**)
frameStr = ""
for c in frame:
    frameFile.write(c)
    frameStr += c

frameFile.close()
# print(type(frameStr))
# print(frameStr)


# (**4**)
frameList = frameStr.split('\n')
print(frameList)

# sys.exit()
labels = {}
values = {}
mesures = []

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
            de.horo = ""
        mesures.append(de)

print('\n\n')
for m in mesures:
    print("%s %s %s" % (m.label, m.value, m.horo))

sys.exit()
