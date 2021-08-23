from __future__ import division
import os
import time
import argparse
import collections


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
    parser.add_argument('-c', dest='convert', required=False,
                        action="store_true",
                        help="converts data to human readable")
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
        outfile = 'memutil.csv'
    if args.convert:
        convert = True
    else:
        convert = False
    return silent, noheader, refresh, runtime, append, outfile, convert


def handle_size(bytes_in=False, bytes_out=False):
    """
    a function that converts bytes to human readable form. returns a
    string like: 42.31 TB. example:
    your_variable_name = make_readable(value_in_bytes)
    """
    tib = 1024 ** 4
    gib = 1024 ** 3
    mib = 1024 ** 2
    kib = 1024
    if bytes_in:
        data = float(bytes_in)
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
        formated_data = "{0:.2f}".format(new_data)
        converted_data = str(formated_data) + symbol
        return converted_data
    elif bytes_out:
        symbol = bytes_out[-1].lower()
        data = bytes_out[0:-1]
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


def get_mem(convert):
    _mem_ = collections.namedtuple('_mem_', ['total', 'used', 'free', 'buff',
                                             'cache', 'slab', 'swap'])
    with open('/proc/meminfo') as f:
        lines = {}
        for line in f:
            x = line.split()
            lines[x[0]] = (int(x[1]) * 1024)
            # if convert:
            #     lines[x[0]] = handle_size(bytes_in=(int(x[1]) * 1024),
            #                               bytes_out=False)
            # else:
            #     lines[x[0]] = (int(x[1]) * 1024)
    total = lines['MemTotal:']
    free = lines['MemFree:']
    buff = lines['Buffers:']
    cache = lines['Cached:']
    slab = lines['Slab:']
    swap_total = lines['SwapTotal:']
    swap_free = lines['SwapFree:']
    swap = int(swap_total) - int(swap_free)
    used = (total - free - buff - cache - slab)
    if convert:
        total = handle_size(bytes_in=total)
        free = handle_size(bytes_in=free)
        buff = handle_size(bytes_in=buff)
        cache = handle_size(bytes_in=cache)
        slab = handle_size(bytes_in=slab)
        used = handle_size(bytes_in=used)
        swap = handle_size(bytes_in=swap)
    mem = _mem_(total, used, free, buff, cache, slab, swap)
    return mem


def write_data(convert, outfile):
    mem = get_mem(convert)
    now = time.time()
    data = "{},{},{},{},{},{},{},{}\n".format(now, mem.total, mem.used,
                                              mem.free, mem.buff, mem.cache,
                                              mem.slab, mem.swap)
    with open(outfile, 'a') as f:
        f.write(data)


def main():
    start = time.time()
    silent, noheader, refresh, runtime, append, outfile, convert = get_args()
    header = "utime,total,used,free,buff,cache,slab,swap\n"
    handle_file(header, noheader, append, outfile)
    uptime = 0
    while uptime <= runtime:
        write_data(convert, outfile)
        time.sleep(refresh)
        uptime = (time.time() - start)


if __name__ == '__main__':
    main()
