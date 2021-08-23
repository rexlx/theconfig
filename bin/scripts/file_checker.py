from __future__ import print_function
import os
import time
import sys
import datetime as dt
import argparse


# --USER-VARIABLES-- #
user_file = 'your_file_here.txt'
# limit can be in bytes or X[k,m,g,t] default is 1GiB
user_limit = (1 * (1024 ** 3))
# wait is in seconds
user_wait = 60
# runtime is in seconds, default is forever
user_runtime = float('inf')
# s is the date string
s = "%Y-%m-%d %H:%M:%S"
# --USER-VARIABLES-- #


def get_args():
    """
    gets cli args via the argparse module
    """
    msg = "monitors a file's size and zeroes it when needed"
    # create an instance of parser from the argparse module
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument(
                        '-f',
                        dest='_file',
                        required=False,
                        help="file to monitor"
                        )
    parser.add_argument(
                        '-l',
                        dest='limit',
                        required=False,
                        help="max file size in bytes or X[k,m,g,t] (15g)"
                        )
    parser.add_argument(
                        '-w',
                        dest='wait',
                        required=False,
                        help="wait interval"
                        )
    parser.add_argument(
                        '-r',
                        dest='runtime',
                        required=False
                        )
    args = parser.parse_args()
    if args._file:
        _file = args._file
    else:
        _file = user_file
    if args.limit:
        limit = args.limit
    else:
        limit = user_limit
    if args.wait:
        wait = float(args.wait)
    else:
        wait = user_wait
    if args.runtime:
        runtime = float(args.runtime)
    else:
        # default runtime is eight hours
        runtime = user_runtime
    return _file, limit, runtime, wait


def handle_size(bytes_in=False, bytes_out=False):
    """
    a function that converts bytes to human readable form, or human
    readable strings into bytes
    """
    # define our symbol sizes here
    tib = 1024 ** 4
    gib = 1024 ** 3
    mib = 1024 ** 2
    kib = 1024
    # if it's bytes_in, we're supplied bytes that we need to convert
    if bytes_in:
        # convert to float
        data = float(bytes_in)
        # divide the size by the symbol size
        if data >= tib:
            symbol = 'TB'
            new_data = data / tib
        elif data >= gib:
            symbol = 'GB'
            new_data = data / gib
        elif data >= mib:
            symbol = 'MB'
            new_data = data / mib
        elif data >= kib:
            symbol = 'KB'
            new_data = data / kib
        elif data >= 0:
            symbol = ' B'
            new_data = data
        # only show two decimals
        formated_data = "{0:.2f}".format(new_data)
        # add our symbol size
        converted_data = str(formated_data) + symbol
        return converted_data
    # otherwise we received a str to convert into bytes
    elif bytes_out:
        # the symbol is the last ch of the str
        symbol = bytes_out[-1].lower()
        # size is the rest
        data = bytes_out[0:-1]
        # try to convert
        try:
            bytes = int(data)
        except Exception as e:
            print("couldnt convert " + data + " to int!")
            print(e)
            exit()
        if symbol == 't':
            converted_data = bytes * tib
        elif symbol == 'g':
            converted_data = bytes * gib
        elif symbol == 'm':
            converted_data = bytes * mib
        elif symbol == 'k':
            converted_data = bytes * kib
        else:
            print("unsupported size type! expected t, g, m, or k!")
            exit()
        return converted_data


def poll_file(_file, limit, runtime, wait, warn=False):
    """
    watch a files size and zero it when the limit has been reached
    if warn is supplied, if the file hasnt grown in the time specified,
    warn the use and continue running
    """
    # init our start time 
    start = time.time()
    # warn_start = start
    uptime = 0
    # warn_time = uptime
    # we use this to know when to warn the user of no growth.
    not_grown = 0
    # this try block handles the file size limit regardless of whether
    # it is bytes or str
    try:
        _limit = int(limit)
    except Exception as e:
        try:
            _limit = handle_size(bytes_in=False, bytes_out=limit)
        except Exception as e:
            print("unexpected error", e)
            exit()
    # how we get the files size
    size = os.path.getsize(_file)
    # uptime is changing dynamically within this loop, runtime is
    # supplied via cli (or defaults)
    while uptime <= runtime:
        uptime = time.time() - start
        # warn_time = time.time() - warn_start
        # if the file has reached its limit, zero it
        if size >= _limit:
            date = dt.datetime.fromtimestamp(time.time()).strftime(s)
            print("\nzeroing file at " + date)
            # this is how we zero the file, "w" implies don't append
            open(_file, 'w').close()
        # get the file size and wait for the supplied wait time, then
        # get the size again
        size = os.path.getsize(_file)
        time.sleep(wait)
        new_size = os.path.getsize(_file)
        # if the size hasnt changed, and warn is not False or 0
        if (new_size - size ) < 1 and warn:
            # then the file hasnt grown, increase our not_grown counter
            not_grown += 1
            # if not_grown has reached it's limit, warn the user and
            # reset the not_grown counter
            if not_grown >= (warn / wait):
                not_grown = 0
                msg = "\n{}: file hasnt grown in {} seconds!"
                print(msg.format(dt.datetime.now(), str(warn)))
        else:
            # otherwise the file has grown, reset our not_grown counter
            not_grown = 0
        # convert our data into human form
        new_size_readable = handle_size(bytes_in=new_size)
        diff = handle_size(bytes_in=(new_size - size))
        # tell the user what's up
        msg = "{}: file is {}, it grew {} in {} seconds.     "
        message = msg.format(
                             str(dt.datetime.now()),
                             str(new_size_readable),
                             str(diff),
                             str(wait)
                             )
        # we write the message to stdout with \r so we dynamically
        # replace the line, instead of getting a new line every time
        # like we would with print()
        sys.stdout.write('%s\r' % message)
        sys.stdout.flush()


# MAIN ENTRY HERE
# if the script is being ran as itself (not being imported)
if __name__ == '__main__':
    # get our args
    _file, limit, runtime, wait = get_args()
    # watch the file
    poll_file(_file, limit, runtime, wait, warn=1200)
    # now we're done
    print('\ncompleted')
