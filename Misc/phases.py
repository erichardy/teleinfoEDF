import machine, neopixel
from time import sleep_ms

"""
phase1 : 0 - 5 ; 6 - 11
phase2 : 12 - 17 ; 18 - 23
phase3 : 24 - 29 ; 30 - 35
"""

class phase():
    """ attributes for rank of leds
    """
    SINSTS = 0
    SMAXSN = 0
    maxBright = 10 # maximum brightness of the LEDs
    startLed_Inst = 0 # LEDs for instantaneous values
    endLed_Inst = 0
    startLed_Max = 0 # LEDs for max value
    endLed_Max = 0
    np = None # neopixel.NeoPixel object
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
        watts = value % 1000
        if kwatts > 0:
            for led in range(startLed, kwatts):
                self.np[led] = self.white
                sleep_ms(10)
                # self.np.write()
        if watts in range(1, 333):
            color = (0, self.maxBright, 0)
        elif watts in range(333, 666):
            color = (0, 0, self.maxBright)
        elif watts in range(666, 1000):
            color = (self.maxBright, 0, 0)
        self.np[kwatts] = color
        self.np.write()

    def displayInst(self):
        self.clearInst()
        self._display(self.SINSTS, self.startLed_Inst)

    def displayMax(self):
        self.clearMax()
        self._display(self.SMAXSN, self.startLed_Max)

