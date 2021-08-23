from __future__ import division
import sys

def make_readable(val):
    """
    a function that converts bytes via base 2 (binary)
    instead of base 10 (decimal) to human readable forms
    """
    data = float(val)
    tib = 1024 ** 4
    gib = 1024 ** 3
    mib = 1024 ** 2
    kib = 1024
    if data >= tib:
        symbol = ' TB'
        new_data = data / tib
    elif data >= gib:
        symbol = ' GB'
        new_data = data / gib
    elif data >= mib:
        symbol = ' MB'
        new_data = data / mib
    elif data >= kib:
        symbol = ' KB'
        new_data = data / kib
    else:
        symbol = ' B'
        new_data = data
    formated_data = "{0:.2f}".format(new_data)
    converted_data = str(formated_data) + symbol
    return converted_data


output = make_readable(sys.argv[1])
print(output)
