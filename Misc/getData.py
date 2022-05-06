"""
si on ne peut faire qu'une lecture en binaire sur l'UART, il faudra :
1/ fd = open(......, 'rb')
2/ encoding = 'utf-8'
3/ val = val.decode(encoding)
"""

def getData(uart):
    frameBytes = []
    val = ''

    if uart.any() > 0:
        val = uart.read(1)
    while(val != b'\x02'):
        if uart.any() > 0:
            val = uart.read(1)
            # sleep_ms(5)

    while(val != b'\x03'):
        frameBytes.append(val)
        if uart.any() > 0:
            val = uart.read(1)
            # sleep_ms(5)

    return(frameBytes)

"""
def getData(uart):
    frameBytes = []
    val = b''

    val = uart.read(1)
    while(ord(val) != 2):
        val = uart.read(1)

    while(ord(val) != 3):
        frameBytes.append(val)
        val = uart.read(1)

    return(frameBytes)
"""

def frameToDict(frameBytes):
    frameSTR = ""
    for c in frameBytes:
        frameSTR += c.decode('ascii')
    frame = frameSTR.split('\n')
    labels = {}
    for data in frame:
        d = data.split('\t')
        if len(d) > 1:
            labels[d[0]] = d[1]
    return(labels)

