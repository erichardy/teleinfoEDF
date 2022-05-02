
from machine import Pin, I2C
from time import sleep_ms

from machine import UART
uart = UART(2, 1200)
even = 0
odd = 1
uart.init(1200, bits=7, parity=even, stop=1)

led = Pin(2, Pin.OUT)

for l in range(65, 92):
    for i in range(0, 200):
        sent = uart.write(chr(l))
        # sleep_ms(1000)

