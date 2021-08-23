"""
A python tool set
"""
import datetime

###
###  bytes to human readable
###

def make_readable(val):
    """
    a function that converts bytes via base 2 (binary)
    instead of base 10 (decimal) to human readable forms
    """
    data = int(val)
    tib = 1024 ** 4
    gib = 1024 ** 3
    mib = 1024 ** 2
    kib = 1024
    if data >= tib:
        symbol = '  TB'
        new_data = data / tib
    elif data >= gib:
        symbol = '  GB'
        new_data = data / gib
    elif data >= mib:
        symbol = '  MB'
        new_data = data / mib
    elif data >= kib:
        symbol = '  kB'
        new_data = data / kib
    else:
        symbol = '  B'
        new_data = data
    formated_data = "{0:.2f}".format(new_data)
    converted_data = str(formated_data).ljust(6) + symbol
    return converted_data

def sec(seconds):
    """
    A python program that converts seconds to
    human readable times
    """
    #Copies the number
    s = int(seconds)

    #Sets default values
    year = 0
    month = 0
    week = 0
    day = 0
    hour = 0
    mins = 0

    # this loop tests the input and breaks
    # it into years, months, weeks, days,
    # hours, and seconds
    while True:
        if s <= 0:
            print("sorry thats zero")
            error = 'true'
            break
        elif s >= 31556952:
            s -= 31556952
            year += 1
            continue
        elif s >= 2628000:
            s -= 2628000
            month += 1
            continue
        elif s >= 603120:
            s -= 603120
            week += 1
            continue
        elif s >= 86160:
            s -= 86160
            day += 1
            continue
        elif s >= 3600:
            s -= 3600
            hour += 1
            continue
        elif s >= 60:
            s -= 60
            mins += 1
            continue
        elif s < 60:
            break
    converted_data = str(year) + "y " + str(week) + "w " + str(day) \
                     + "d " + str(hour) + "h " + str(mins) + "m " \
                     + str(s) + "s"
    return converted_data

##
##  unit conversion
##

# conevrt epoch
def convert_epoch(x):
    """
    converts epoch (unix) time to date
    """
    converted_data = datetime.datetime.fromtimestamp(x).strftime(
    '%Y-%m-%d %H:%M:%S')
    return converted_data

# digital conversion
def by2kby(val):
    x = val / 1024
    return x

def b2mb(val):
    x = val / ( 1024 ** 2 )
    return x

def b2gb(val):
    x = val / ( 1024 ** 3 )
    return x

def b2tb(val):
    x = val / ( 1024 ** 4 )
    return x

def tb2b(val):
    x = val * ( 1024 ** 4 )
    return x

def gb2b(val):
    x = val * ( 1024 ** 3 )
    return x

def mb2b(val):
    x = val * ( 1024 ** 2 )
    return x

def kb2b(val):
    x = val * 1024
    return x

def kb2mb(val):
    x = val / 1024
    return x

def kb2gb(val):
    x = val / ( 1024 ** 2 )
    return x

def kb2tb(val):
    x = val / ( 1024 ** 3 )
    return x

def tb2kb(val):
    x = val * ( 1024 ** 3 )
    return x

def gb2kb(val):
    x = val * ( 1024 ** 2 )
    return x

def mb2kb(val):
    x = val * 1024
    return x
