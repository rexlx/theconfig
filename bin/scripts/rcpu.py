from __future__ import print_function
from __future__ import division
import re, time, psutil, sys, platform, os, argparse

"""
description:

this script gathers the cpu stats and average cpu speed for all cores.
to get the cpu speed you must be on a non-virtualized machine running
linux. the script will detect the ability to collect the cpu speed.
writes all data to to a csv named cpuutil.plot

example:

$ python rcpu.py -h
usage: rcpu.py [-h] [-s] [-n] [-R REFRESH] [-r RUNTIME]

This script records cpu statistics

optional arguments:
  -h, --help  show this help message and exit
  -s          dont display statistics to screen
  -n          dont write header
  -R REFRESH
  -r RUNTIME

csv example:
$ head cpuutil.plot
utime,load,speed
1544389258.45,0.0,2489.77775
"""


def get_args():
    """
    gets cli args via the argparse module
    """
    msg = "This script records cpu statistics"
    # create an instance of parser from the argparse module
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-s', dest='silent', required=False,
                        action="store_true",
                        help="dont display statistics to screen")
    parser.add_argument('-a', dest='append', required=False,
                        action="store_true",
                        help="dont overwrite previous files")
    parser.add_argument('-n', dest='noheader', required=False,
                        action="store_true", help="dont write header")
    parser.add_argument('-R', dest='refresh', required=False)
    parser.add_argument('-r', dest='runtime', required=False)
    parser.add_argument('-o', dest='outfile', required=False)
    args = parser.parse_args()
    if args.silent:
        silent = True
    else:
        silent = False
    if args.noheader:
        noheader = True
    else:
        noheader = False
    if args.append:
        append = True
    else:
        append = False
    if args.refresh:
        refresh = float(args.refresh)
    else:
        # default refresh i s 5 seconds
        refresh = 5
    if args.runtime:
        runtime = float(args.runtime)
    else:
        # default runtime is eight hours
        runtime = 28800
    if args.outfile:
        outfile = args.outfile
    else:
        outfile = 'cpuutil.plot'
    return silent, noheader, refresh, runtime, append, outfile


def handle_file(header, noheader, append, outfile):
    """
    handles file removal and headers
    """
    # if they want a fresh file
    if not append:
        try:
            # remove the old outfile
            os.remove(outfile)
            # if the want a header
            if not noheader:
                # give it to them
                with open(outfile, 'w') as f:
                    f.write(header)
        except Exception as e:
            # exception is likely file doesnt exist
            print(e, " continuing...\n")
            # in which case, nothing to remove, write the header if
            # they want it. other issue would be permissions, in which
            # case we cant write to the file anyways
            if not noheader:
                with open(outfile, 'w') as f:
                    f.write(header)


def get_dist():
    """
    this function gets the os and determines if the machine
    is real or virtual
    """
    # the cpuinfo file on linux systems
    cpuinfo = '/proc/cpuinfo'
    # get the platform
    poll_type = platform.system()
    if poll_type == 'Windows':
        return poll_type
    # this block tests /proc/cpuinfo for the hypervisor flag, which
    # means the system is a VM and wont be able to detect freq
    # this has no control for detecting mac as i have none to test on
    elif os.path.isfile(cpuinfo):
        try:
            with open(cpuinfo) as f:
                matches = re.findall(r'hypervisor', f.read())
                if len(matches) > 0:
                    poll_type = matches[-1]
                    return poll_type
                else:
                    return poll_type
        except Exception as e:
            print('couldnt open /proc/cpuinfo!', e)
            sys.exit()


def poll_cpu(refresh, poll_type, outfile):
    """
    this function gathers the cpu usage and frequency (freq doesnt work on
    windows) once a second per refresh period(rate) and updates the screen
    once every refresh period. it then writes all per second poll / freq data
    to a csv file.
    """
    times = []
    loads = []
    speeds = []
    count = 0
    while count < refresh:
        # if the machine isnt linux and real, we cant record the cpu
        # frequency
        if poll_type == 'Windows' or poll_type == 'hypervisor':
            # mark the time
            now = str(time.time())
            times.append(now)
            # get the cpu usage
            x = psutil.cpu_percent(interval=None, percpu=False)
            # add it to the load list
            loads.append(x)
        else:
            # we can get all the data
            # mark the time
            now = str(time.time())
            times.append(now)
            # get the cpu usage
            x = psutil.cpu_percent(interval=None, percpu=False)
            # add it to the load list
            loads.append(x)
            # get the cpu speed
            freq = psutil.cpu_freq()
            # i only care about the current speed
            cpu_speed = freq.current
            # append the speeds list
            speeds.append(cpu_speed)
        # wait a second and increment. repeat.
        time.sleep(1)
        count += 1
    # determine the average usage for period
    cpu_avg = sum(loads) / len(loads)
    # determine low / high speed for poll period
    if len(speeds) > 0:
        min_speed, max_speed = min(speeds), max(speeds)
        # dump data into a csv(,)
        # unixtime,load,frequency(linux only)
        with open(outfile, 'a') as f:
            for i in range(0, len(loads)):
                f.write(str(times[i]) + ',' + str(loads[i]) +
                        ',' + str(speeds[i]) + '\n')
        return cpu_avg, min_speed, max_speed
    else:
        # unixtime,load
        with open(outfile, 'a') as f:
            for i in range(0, len(loads)):
                f.write(str(times[i]) + ',' + str(loads[i]) + '\n')
        return cpu_avg


def main(silent, noheader, refresh, runtime, append, outfile):
    poll_type = get_dist()
    uptime = 0
    start = time.time()
    # headers will differ based on system type, test and adjust
    if poll_type == 'Linux':
        header = 'utime,load,speed\n'
    else:
        header = 'utime,load\n'
    # call the handle file function
    handle_file(header, noheader, append, outfile)
    while uptime <= runtime:
        # i could probably test for Linux, but knowing how these things
        # go, theres some distro out there that breaks this test
        if poll_type != 'Windows' and poll_type != 'hypervisor':
            # unpack the values from poll_cpu
            load, min_freq, max_freq = poll_cpu(refresh, poll_type, outfile)
            # create the display message
            data = "average usage: " + str(round(load, 2)) + \
                   " cpu speed min/max: " + str(round(min_freq, 2)) + '/' + \
                   str(round(max_freq, 2))
            if not silent:
                # if they dont provide the -s flag, print the values to
                # same line (overwriting the previous line)
                sys.stdout.write('%s\r' % data)
                sys.stdout.flush()
        else:
            load = poll_cpu(refresh, poll_type, outfile)
            data = format(load, '.2f')
            msg = "percent used:  " + str(data) + ' '
            if not silent:
                sys.stdout.write('%s\r' % msg)
                sys.stdout.flush()
        now = time.time()
        uptime = now - start


if __name__ == '__main__':
    silent, noheader, refresh, runtime, append, outfile = get_args()
    main(silent, noheader, refresh, runtime, append, outfile)
    print('\n')
