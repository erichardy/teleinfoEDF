from datetime import datetime

def toDate(strDate):
    # strDate is like : "E221019225938"
    #                     123456789012
    y = int(strDate[1:3])
    m = int(strDate[3:5])
    d = int(strDate[5:7])
    h = int(strDate[7:9])
    m = int(strDate[9:11])
    s = int(strDate[11:13])
    theDate = datetime(y, m, d, h, m, s)
    # we can get separate parameters with datetime object as :
    # theDate.year  theDate.month, etc... with day, hour, minute, second
    return theDate

