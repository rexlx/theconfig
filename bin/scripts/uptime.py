import sys
import socket

def seconds_to_readable(seconds):
    """
    A python program that converts seconds to
    human readable times
    """
    #Copies the number
    s = int(float(seconds))

    #Sets default values
    day = 0
    hour = 0
    mins = 0

    # this loop tests the input and breaks
    # it into years, months, weeks, days,
    # hours, and seconds
    while True:
        if s < 0:
            print("thats less then zero...")
            error = 'true'
            break
        elif s >= 86400:
            s -= 86400
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
    converted_time = str(day).rjust(4) + 'd ' + str(hour).rjust(3) + 'h ' \
                   + str(mins).rjust(3) + 'm ' + str(s).rjust(3) + 's'
    print(socket.gethostname().ljust(36) + ' ' + converted_time)


f = open('/proc/uptime', 'r')
vals = []

for i in f:
    line = str(i).split()
    uptime = line[0]

seconds_to_readable(uptime)
