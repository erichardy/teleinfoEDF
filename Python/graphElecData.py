#!/usr/bin/python3

import argparse
import datetime as dt
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from sys import exit
from sys import version_info
from getEDFdata import toDate

if version_info.minor < 6:
    print("Python version must be >= 3.6")
    exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--buffer_size", type=int, help="Size of the buffer", default=60)
parser.add_argument("-d", "--device", type=str, help="USB/Serial device", default="/dev/ttyUSB0")
parser.add_argument("-m", "--max_delta", type=int, help="delta between to recorded data", default=5)
parser.add_argument("-f", "--filename", type=str, help="file name where to save data", default=None)
args = parser.parse_args()

_size = args.buffer_size
_dataFilename = args.filename
_dataFile = None

if _dataFilename is not None:
    try:
        now = dt.datetime.now().strftime("-%y%m%d%H%M%S")
        _dataFile = open(_dataFilename + now, "a")
    except:
        print("Unable to open %s to add data !!!" % (_dataFilename))
        _dataFile = None
        _dataFilename = None

    
SERIAL_DEV = args.device
ser = serial.Serial(SERIAL_DEV , 9600, parity=serial.PARITY_EVEN)
ser.bytesize = serial.SEVENBITS
ser.stopbits = serial.STOPBITS_ONE

_prev_m = '0'
_nb = 0
_nbRecorded = 0

# Create figure for plotting
fig = plt.figure(figsize=[10, 4])
ax = fig.add_subplot(1, 1, 1)
# print(fig.canvas.get_renderer())
# print(ax.get_tightbbox(fig.canvas.get_renderer()))
#       Bbox(x0=93.15277777777777, y0=20.27777777777777, x1=911.0625, y1=357.5)
ts = []
p1 = []
p2 = []
p3 = []
labels = []

# _yLimits = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
_yLimits = np.arange(200, 6000, 200).tolist()
_LyLimits = len(_yLimits)

# _size = 80
# _size = 70
_nbReads = 0
_prevData = (" ", " ", 1, 1, 1)
MAX_DELTA = args.max_delta # watts


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
        print("len(fSTR) != 1213 : %i" % (len(fSTR)))
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


# to fix in case of None type object
def getDataLine():
    f = getOneFrame()
    (val, horos, checksums) = getDict(f)
    try:
        DATE = toDate(horos['DATE']).isoformat(' ', timespec='seconds')
        SINSTS1 = val['SINSTS1']
        SINSTS2 = val['SINSTS2']
        SINSTS3 = val['SINSTS3']
        l = DATE + ' ' + SINSTS1 + ' ' + SINSTS2 + ' ' + SINSTS3
        return l
    except:
        return None


def maxValue(l1, l2, l3):
    highValue = max([max(l1), max(l2), max(l3)])
    for v in _yLimits:
        if highValue < v:
            return v
    return 6500

def recordData(cur):
    global _nbRecorded
    global _dataFile
    _nbRecorded += 1
    if _dataFile is None:
        print("%s %s %i %i %i (%i/%i)" % (
            cur[0], cur[1], cur[2], cur[3], cur[4], _nbRecorded, _nb))
    else:
        data = ("%s %s %i %i %i %i\n") % (cur[0], cur[1], cur[2], cur[3], cur[4], _nb)
        _dataFile.write(data)
        if _nb - _nbRecorded > 19:
            _dataFile.flush()

# we record current data if one of the phase has a diff of MAX_DELTA
# with the previous recorded data
def recordedData(cur, prev):
    if abs(cur[2] - prev[2]) > MAX_DELTA:
        recordData(cur)
        return(cur)
    if abs(cur[3] - prev[3]) > MAX_DELTA:
        recordData(cur)
        return(cur)
    if abs(cur[4] - prev[4]) > MAX_DELTA:
        recordData(cur)
        return(cur)
    return prev

# This function is called periodically from FuncAnimation
def animate(i, ts, p1, p2, p3, labels):

    global _prev_m
    global _size
    global _nb
    global _nbReads
    global _prevData

    l  = getDataLine()
    # _nbReads += 1
    _nb += 1
    if not l:
        error_date = dt.datetime.now()
        print("%s : Erreur retour de getDataLine : %s" % (str(_nb), str(error_date)))
        return
    ll = l.split(' ')
    day = ll[0]
    t = ll[1]
    tt = t.split(':')
    h = tt[0]
    m = tt[1]
    
    ph1 = int(ll[2])
    ph2 = int(ll[3])
    ph3 = int(ll[4])
    # Add x and y to lists
    ts.append(t)
    p1.append(ph1)
    p2.append(ph2)
    p3.append(ph3)
    if m != _prev_m:
        labels.append(t)
    else:
        labels.append(' ')
    curData = (day, t, ph1, ph2, ph3)
    _prevData = recordedData(curData, _prevData)
    # Limit x and y lists to 20 items
    # p1 = p1[_size:]
    p1 = p1[-_size:]
    p2 = p2[-_size:]
    p3 = p3[-_size:]
    ts = ts[-_size:]
    labels = labels[-_size:]

    # Draw x and y lists
    ylimit = maxValue(p1, p2, p3)
    ax.clear()
    # auto-scale on y axis
    ax.axis([1, _size, 0, ylimit])

    phase1, = ax.plot(ts, p1, label='ph 1', color='blue')
    phase2, = ax.plot(ts, p2, label='ph 2', c='green')
    phase3, = ax.plot(ts, p3, label='ph 3', c='red')
    legends = ['phase 1 : ' + str(ph1), 'phase 2 : ' + str(ph2), 'phase 3 : '+ str(ph3)]
    ax.legend(handles=[phase1, phase2, phase3], labels=legends)
    # ax.annotate("annotation", (0, 1500))

    # Format plot
    plt.xticks(ticks=ts, labels=labels, rotation=20, ha='right')
    _prev_m = m
    plt.subplots_adjust(right=0.98, left=0.08, top=0.90, bottom=0.10)
    plt.title("Consommation élec par phase (temps réel) " + day + ' ' + t + ' ' + str(_nb))
    plt.ylabel("Watts")
    # print(ax.get_legend_handles_labels())
    # sleep(.3)

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ts, p1, p2, p3, labels), interval=50)
plt.show()

