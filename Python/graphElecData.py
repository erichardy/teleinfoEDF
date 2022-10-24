#!/usr/bin/python3

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from getEDFdata import getDataLine
from sys import exit

_prev_m = '0'

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

_yLimits = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
_LyLimits = len(_yLimits)

_size = 80

def maxValue(l1, l2, l3):
    highValue = max([max(l1), max(l2), max(l3)])
    for v in _yLimits:
        if highValue < v:
            return v
    return 6500

# This function is called periodically from FuncAnimation
def animate(i, ts, p1, p2, p3, labels):

    global _prev_m
    global _size

    l  = getDataLine()
    if not l:
        error_date = dt.datetime.now()
        print("Erreur retour de getDataLine : " + str(error_date))
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
    plt.title("Consommation élec par phase (temps réel) " + day + ' ' + t)
    plt.ylabel("Watts")
    # print(ax.get_legend_handles_labels())

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ts, p1, p2, p3, labels), interval=50)
plt.show()

