"""
si on ne peut faire qu'une lecture en binaire sur l'UART, il faudra :
1/ fd = open(......, 'rb')
2/ encoding = 'utf-8'
3/ val = val.decode(encoding)
"""


def getData(uart):
    frameBytes = []
    val = b''

    if uart.any() > 0:
        val = uart.read(1)
    while(ord(val) != 2):
        if uart.any() > 0:
            val = uart.read(1)

    while(ord(val) != 3):
        frameBytes.append(val)
        if uart.any() > 0:
            val = uart.read(1)

    return(frameBytes)


def frameToDict(frameBytes):
    frameSRT = ""
    for c in frameBytes:
        frameSTR += c.decode('utf-8')
    frame = frameSTR.split('\n')
    labels = {}
    for data in frame:
        d = data.split('\t')
        labels[d[0]] = d[1]
    return(labels)

