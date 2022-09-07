
import micropython as upy
from gc import mem_free
from gc import mem_alloc

import machine
from gc import enable
from gc import collect
from os import remove
from getFrame import getFrame, getDict
from phases import phase
from time import sleep_ms

buzzer = 13 # buzzer on Pin 13
p_buzzer = machine.Pin(buzzer, machine.Pin.OUT)


def alarm(times):
    for i in range(0, times):
        p_buzzer.on()
        sleep_ms(50)
        p_buzzer.off()
        sleep_ms(50)


RATE = 9600
# uart = UART(2, baudrate=9600)
# uart.init( baudrate=9600, bits=7, parity=0, stop=1)
uart = machine.UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)

enable()
phase1 = phase()
phase2 = phase()
phase3 = phase()

try:
    reseted = open('reseted', "r")
    alarm(100)
    remove('reseted')
except:
    pass

alarm(3)
sleep_ms(2000)
alarm(3)
n = 0
# for n in range(0, 50):
while (1):
    collect()
    f = getFrame(uart)
    (v, h, c) = getDict(f)
    try:
        date = h['DATE']
        print("Date : %s %i" % (date, n))
        # print("free : %i ; alloc %i" % (mem_free(), mem_alloc()))
        if v:
            phase1.SINSTS = int(v['SINSTS1'])
            phase1.SMAXSN = int(v['SMAXSN1'])
            phase2.SINSTS = int(v['SINSTS2'])
            phase2.SMAXSN = int(v['SMAXSN2'])
            phase3.SINSTS = int(v['SINSTS3'])
            phase3.SMAXSN = int(v['SMAXSN3'])
    except:
        print("No date !!! %i" % (n))
    n += 1
    """
    print("Date : %s" % (h['DATE']))
    print("phase 1 : %i %i\n" % (phase1.SINSTS, phase1.SMAXSN))
    print("phase 2 : %i %i\n" % (phase2.SINSTS, phase2.SMAXSN))
    print("phase 3 : %i %i\n" % (phase3.SINSTS, phase3.SMAXSN))
    """
    """
    for horo in h.keys():
        print("%s %s" % (horo, h[horo]))
    for val in v.keys():
        print("%s %s" % (val, v[val]))
    for check in c.keys():
        print("%s %s" % (check, c[check]))
    """
alarm(3)
sleep_ms(2000)
alarm(3)

# print(upy.mem_info())
# print("free : %i ; alloc %i" % (mem_free(), mem_alloc()))
# print("Fin")
