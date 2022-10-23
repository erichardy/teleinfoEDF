import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from getEDFdata import getDataLine
from sys import exit

_prev_m = '0'

"""
f = open("dataEDF", 'r')

def getLine(f):
    l = f.readline()
    if l:
        return l
    else:
        return None
"""


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
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
    ll = l.split(' ')
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

    ax.plot(ts, p1, label='ph 1', color='blue')
    ax.plot(ts, p2, label='ph 2', c='green')
    ax.plot(ts, p3, label='ph 3', c='red')
    ax.legend()

    # Format plot
    """
    Need to solve labels issue :
    I don't want a label for each value but for each minute change,
    the label animated accordingly the values !
    if m != _prev_m:
        labels.append(t)
    else:
        labels.append(' ')
    """
    labels.append(t)
    plt.xticks(ticks=ts, rotation=45, ha='right')
    _prev_m = m
    plt.subplots_adjust(bottom=0.30)
    plt.title('Consommation électrique par phase en temps réel')
    plt.ylabel('Watts')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(ts, p1, p2, p3, labels), interval=50)
plt.show()

