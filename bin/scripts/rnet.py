import psutil as ps
import time, os, sys, argparse

"""
description:

this script collects network statistics. it saves the file as csv(,)

todo:
it would be better if regardless of the refresh rate, it still writes
per second stats to a file.

example:

$ python rnet.py -h
usage: rnet.py [-h] [-s] [-n] [-R REFRESH] [-r RUNTIME]

This script records network statistics

optional arguments:
-h, --help  show this help message and exit
-s          dont display statistics
-n          dont write header
-R REFRESH
-r RUNTIME

sample csv output:

utime,recv,sent,err_in,err_out
1544481320.25,186,168,0,0
"""


def get_args():
    # create parser
    msg = "This script records network statistics"
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
        outfile = 'net.plot'
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


def make_readable(val):
    """
    a function that converts bytes to human readable form, returns a
    string like: 42.31 TB
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
    # we only care about two decimal places
    formated_data = "{0:.2f}".format(new_data)
    converted_data = str(formated_data).ljust(6) + symbol
    return converted_data


def net_poll(poll_time):
    """
    get both system wide stats and per nic stats. sleeps for the poll
    time, gets them again. returns them
    """
    sys_wide_start = ps.net_io_counters(pernic=False)
    # will eventually add per nic support
    per_nic_start = ps.net_io_counters(pernic=True)
    time.sleep(poll_time)
    sys_wide_end = ps.net_io_counters(pernic=False)
    per_nic_end = ps.net_io_counters(pernic=True)
    return sys_wide_start, per_nic_start, sys_wide_end, per_nic_end


def crunch_data(refresh, silent, outfile):
    # get the network statistics
    sys_start, by_nic_start, sys_end, by_nic_end = net_poll(refresh)
    recv_start = sys_start.bytes_recv
    recv_end = sys_end.bytes_recv
    sent_start = sys_start.bytes_sent
    sent_end = sys_end.bytes_sent
    error_in = sys_end.dropin
    error_out = sys_end.dropout
    # determine the difference
    recv_data = recv_end - recv_start
    sent_data = sent_end - sent_start
    total_recv = make_readable(recv_data)
    total_sent = make_readable(sent_data)
    # get the time
    now = str(time.time())
    # write the data to a csv
    with open(outfile, 'a') as f:
        f.write(now + ',' + str(recv_data) + ',' + str(sent_data) + ',' +
                str(error_in) + ',' + str(error_out) + '\n')
    # display stats
    if not silent:
        msg = "sent/recv: " + str(total_sent) + '/' + str(total_recv) + \
              '  errors i/o: ' + str(error_in) + ' / ' + str(error_out)
        sys.stdout.write('%s\r' % msg)
        sys.stdout.flush()


def main():
    header = 'utime,recv,sent,err_in,err_out\n'
    # mark the time
    start = time.time()
    # get the args
    silent, noheader, refresh, runtime, append, outfile = get_args()
    _runtime = runtime
    handle_file(header, noheader, append, outfile)
    # initialize uptime
    uptime = 0
    while uptime <= _runtime:
        crunch_data(refresh, silent, outfile)
        now = time.time()
        uptime = now - start
    print('\n')


if __name__ == '__main__':
    main()
