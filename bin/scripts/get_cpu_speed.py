import os
import time
import argparse
import multiprocessing as mp

"""
description:

this script opens /proc/cpuinfo and gets the current mhz as an integer. then,
after adding a header line, writes the data to a csv. the cpu speed can only be
obtained on bare metal machines (not virtualized), and even then, some machines
have bios features that may control the speed and therefore obscure that
information to the OS.

example:

python get_cpu_speed.py -h
usage: get_cpu_speed.py [-h] [-n] [-r RUNTIME]

This script records cpu statistics

optional arguments:
  -h, --help  show this help message and exit
  -n          dont write header
  -r RUNTIME  how long to run in seconds

creates a file 'cpu_speeds.csv'

utime,cpu0,cpu1,cpu2,cpu3,(etc...),avg
1544279626.23,2749,3005,2429,2889,2768
"""


def get_args():
    """
    gets the cli args via argparse
    """
    # exaplin script purpose if help invoked
    msg = "This script records per core cpu speeds"
    # create an instance of argparse
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-n', dest='noheader', required=False,
                        action="store_true", help="dont write header")
    parser.add_argument('-r', dest='runtime', required=False,
                        help="how long to run in seconds")
    # parse args
    args = parser.parse_args()
    # either they want the header or they dont
    if args.noheader:
        noheader = True
    else:
        noheader = False
    # if no runtime is specified, use default
    if args.runtime:
        runtime = float(args.runtime)
    else:
        # default runtime is eight hours
        runtime = 28800
    return noheader, runtime


def cpu_speeds():
    """
    gets the current cpu speed for each processor via /proc/cpuinfo
    returns unixtime and cpu speeds as python list
    """
    # where the cpu info is
    with open('/proc/cpuinfo') as f:
        # create an empty list for later
        speeds = []
        for line in f:
            # get the unix time via time module
            utime = time.time()
            # we only care about the cpu frequency line
            if 'MHz' in line:
                # split the line up into indexes
                x = line.split()
                # convert the indexed string to a float and then to int
                # to shed the decimals
                speed = int(float(x[3]))
                # add it to the list
                speeds.append(speed)
                avg = sum(speeds) / len(speeds)
    return utime, speeds, avg


def write_header():
    # get the total cores (including hyperthreaded ones)
    total_cores = mp.cpu_count()
    # list comprehension that concatenates 'cpu' + core number + ','
    # calculated from the range function 0-total_cores
    cpus = ['cpu' + str(e) + ',' for e in range(0, total_cores)]
    # we dont want the last comma--> OLD solution keeping in case
    # #cpus[-1] = cpus[-1].rstrip(',')
    with open('cpu_speeds.csv', 'a') as fname:
        # write the csv header
        fname.write('utime,')
        for i in cpus:
            fname.write(i)
        fname.write('avg')
        fname.write('\n')


def append_csv(utime, speeds, avg):
    """
    this takes two parameters, utime and speeds, writes data to a csv
    named cpu_speeds.csv. the rows are as follows:
    unixtime,cpu0,cpu1,cpu2,cpu3,etc.....
    """
    with open('cpu_speeds.csv', 'a') as f:
        # write the unixtime (no newline))
        f.write(str(utime) + ',')
        # write all cpu data except the last one + ,
        # #for i in speeds[0:-1]:
        for i in speeds:
            f.write(str(i) + ',')
        # write the final cpu data
        # #f.write(speeds[-1])
        f.write(str(avg))
        # finally, add the newline
        f.write('\n')


def main(noheader, runtime):
    """
    this function adds the header bar to the csv, gets the cpu speeds,
    and then writes it to a csv. takes two arguments as parametes:
    noheader -> boolean (dont write a header to the csv)
    runtime  -> numeric (how long to runfor)
    """
    # mark the start time
    then = time.time()
    # initialize length for the while loop below
    length = 0
    # we dont want to append an old file and mix results, remove.
    try:
        os.remove('cpu_speeds.csv')
    # either the file doesnt exist or we have permission problems
    except Exception as e:
        err = e.args[0]
        if err == 2:
            pass
        elif err == 13:
            print('encountered a permission issue, wont continue...\n')
            return
        else:
            print(e)
            print('continuing...\n')
            pass
    # if the user does not add the -n arg then noheader is False
    if not noheader:
        write_header()
    # main loop
    while length <= runtime:
        # unpack the return of cpu_speeds
        utime, speeds, avg = cpu_speeds()
        # feed that into make_csv
        append_csv(utime, speeds, avg)
        # wait
        time.sleep(1)
        # determine runtime
        now = time.time()
        length = now - then


if __name__ == "__main__":
    noheader, runtime = get_args()
    main(noheader, runtime)
