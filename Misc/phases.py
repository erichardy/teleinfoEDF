import machine, neopixel
from time import sleep
from time import sleep_ms

class phase():
    """ attributes for rank of leds
    """
    maxBright = 10 # maximum brightness of the LEDs
    startLed_Inst = 0 # LEDs for instantaneous values
    endLed_Inst = 0
    startLed_Max = 0 # LEDs for max value
    endLed_Max = 0
    np = None # neopixel.NeoPixel object
    # white = (self.maxBright, self.maxBright, self.maxBright)
    white = (maxBright, maxBright, maxBright)

    def ___init___(self):
        self.clearInst()
        self.clearMax()

    # clear all the LEDs of this phase for instantaneous values
    def clearInst(self):
        for led in range(self.startLed_Inst, self.endLed_Inst + 1):
            self.np[led] = (0, 0, 0)
            self.np.write()
            sleep_ms(10)
        
    # clear all the LEDs of this phase for MAX values
    def clearMax(self):
        for led in range(self.startLed_Max, self.endLed_Max + 1):
            self.np[led] = (0, 0, 0)
            self.np.write()
            sleep_ms(10)

    # light on the LEDs depending of the value
    def _display(self, value, startLed):
        color = (0, 0, 0)
        if value == 0:
            color = (0, 0, 0)
        kwatts = startLed + (value // 1000)
        print(kwatts)
        # watts = value - (kwatts * 1000)
        watts = value % 1000
        if kwatts > 0:
            for led in range(startLed, kwatts):
                self.np[led] = self.white
                sleep_ms(100)
                # self.np.write()
        if watts in range(1, 333):
            color = (0, self.maxBright, 0)
        elif watts in range(333, 666):
            color = (0, 0, self.maxBright)
        elif watts in range(666, 1000):
            color = (self.maxBright, 0, 0)
        self.np[kwatts] = color
        self.np.write()
        print(color)

    def displayInst(self, value):
        self.clearInst()
        self._display(value, self.startLed_Inst)

    def displayMax(self, value):
        self.clearMax()
        self._display(value, self.startLed_Max)

np = neopixel.NeoPixel(machine.Pin(4), 36)

phase1 = phase()
phase1.startLed_Inst = 0
phase1.endLed_Inst = 5
phase1.startLed_Max = 30
phase1.endLed_Max = 35
phase1.np = np

values = [5999, 5550, 5220,
    4999, 4550, 4220, 0,
    3999, 3550, 3220,
    2999, 2550, 2220,
    1999, 1550, 1220,
    999, 550, 220, 0]
"""
for v in values:
    phase1.displayInst(v)
    sleep_ms(100)
"""
""" """
for v in values:
    phase1.displayMax(v)
    sleep_ms(100)
""" """
