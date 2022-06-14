import machine, neopixel
from time import sleep_ms


def cl():
    for l in range(0, 36):
        np[l] = (0, 0, 0)
        np.write()
        sleep_ms(20)
"""
for i in range(0, 100, 5):
    for j in range(0, 100, 5):
        for k in range(0,100, 5):
            np[0] = (i, j, k)
            sleep_ms(2)
            np.write()

"""
np = neopixel.NeoPixel(machine.Pin(4), 36)

for l in range(0, 36):
    np[l] = (10, 10, 10)
    np.write()
    sleep_ms(100)

sleep_ms(2000)

cl()
for l in range(30, 20, -1):
    np[l] = (10, 10, 10)
    np.write()
    sleep_ms(100)

sleep_ms(2000)
cl()

