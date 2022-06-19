
import micropython as upy
from gc import mem_free
from gc import mem_alloc

import machine
import neopixel
from gc import enable
from gc import collect
from os import remove
from getFrame import getFrame, getDict
from phases import phase


RATE = 9600
# uart = UART(2, baudrate=9600)
# uart.init( baudrate=9600, bits=7, parity=0, stop=1)
uart = machine.UART(2, baudrate=RATE) # UART2 default : tx = GPIO17 , rx = GPIO16
even = 0
uart.init(baudrate=RATE, bits=7, parity=even, stop=1)

np = neopixel.NeoPixel(machine.Pin(4), 36)

enable()
"""
phase1 : 0 - 5 ; 6 - 11
phase2 : 12 - 17 ; 18 - 23
phase3 : 24 - 29 ; 30 - 35
"""
phase1 = phase()
phase1.startLed_Inst = 0
phase1.endLed_Inst = 5
phase1.startLed_Max = 6
phase1.endLed_Max = 1
phase1.np = np

phase2 = phase()
phase2.startLed_Inst = 12
phase2.endLed_Inst = 17
phase2.startLed_Max = 18
phase2.endLed_Max = 23
phase2.np = np

phase3 = phase()
phase3.startLed_Inst = 24
phase3.endLed_Inst = 29
phase3.startLed_Max = 30
phase3.endLed_Max = 35
phase3.np = np

for n in range(0, 200):
    # collect()
    # print(upy.mem_info())
    print('-----------')
    print("free : %i ; alloc %i" % (mem_free(), mem_alloc()))
    f = getFrame(uart)
    (v, h, c) = getDict(f)
    collect()
    print("free : %i ; alloc %i" % (mem_free(), mem_alloc()))
    if v:
        phase1.SINSTS = int(v['SINSTS1'])
        phase1.SMAXSN = int(v['SMAXSN1'])
        phase2.SINSTS = int(v['SINSTS2'])
        phase2.SMAXSN = int(v['SMAXSN2'])
        phase3.SINSTS = int(v['SINSTS3'])
        phase3.SMAXSN = int(v['SMAXSN3'])
        phase1.displayInst()
        phase1.displayMax()
        phase2.displayInst()
        phase2.displayMax()
        phase3.displayInst()
        phase3.displayMax()

    print(":%i:" % (n))
    print("phase1 : %i , %i" % (phase1.SINSTS, phase1.SMAXSN))
    print("phase2 : %i , %i" % (phase2.SINSTS, phase2.SMAXSN))
    print("phase3 : %i , %i" % (phase3.SINSTS, phase3.SMAXSN))

# print(upy.mem_info())
print("free : %i ; alloc %i" % (mem_free(), mem_alloc()))
# print(mem_free())
# print(mem_alloc())
