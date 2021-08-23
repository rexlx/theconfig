import subprocess as proc
import argparse
import os
import time
import csv
import sys


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
        outfile = 'pcpu.csv'
    return silent, noheader, refresh, runtime, append, outfile


def get_pcpu():
    cmd = "ps -eo pcpu,args | grep -E 'python'"
    x = proc.Popen(cmd, shell=True, stdout=proc.PIPE)
    o, e = x.communicate()
    data = o.decode('ascii').splitlines()
    new_list = []
    for line in data:
        new_list.append(line.split())
    # results = ','.join([str(e[0]) for e in new_list])
    return new_list


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
                with open(outfile, 'a') as f:
                    f.write(header)
                    f.write(',avg,min,max\n')
        except Exception as e:
            # exception is likely file doesnt exist
            print(e, " continuing...\n")
            # in which case, nothing to remove, write the header if
            # they want it. other issue would be permissions, in which
            # case we cant write to the file anyways
            if not noheader:
                with open(outfile, 'a') as f:
                    f.write(header)
                    f.write('\n')


def main():
    start = time.time()
    uptime = 0
    headers = ['conf' + str(e) for e in range(0, 10)]
    header = ','.join(headers)
    silent, noheader, refresh, runtime, append, outfile = get_args()
    handle_file(header, noheader, append, outfile)
    while uptime <= runtime:
        x = get_pcpu()
        results = [float(e[0]) for e in x]
        if len(results) == 10:
            _avg = float("{0:.2f}".format(sum(results) / len(results)))
            _min, _max = min(results), max(results)
            results.extend((_avg, _min, _max))
            # print(results)
        elif len(results) != 10 and len(results) > 0:
            _avg = float("{0:.2f}".format(sum(results) / len(results)))
            _min, _max = min(results), max(results)
            pad = 10 - len(results)
            results.extend(([None] * pad))
            results.extend((_avg, _min, _max))
        else:
            results = [None] * 13
            _avg, _min, _max = 0, 0, 0
        # #csv_data = ','.join([str(e) for e in results])
        with open(outfile, 'ab') as f:
            wr = csv.writer(f)
            wr.writerow(results)
        if not silent:
            stats = 'avg: {} min: {} max: {}'.format(_avg, _min, _max)
            sys.stdout.write('%s\r' % stats)
            sys.stdout.flush()
        time.sleep(refresh)
        uptime = time.time() - start


if __name__ == '__main__':
    main()


# if we want to go dictionary approach
# #pcpu_stats = {}
# #for i in new_list:
#    #pcpu_stats[str(i[2][-5:])] = str(i[0])

# for i in header:
#    print(pcpu_stats[i], end = " ")
# with open('test.csv', 'a') as f:
#         f.write([str(e) + ',' for e in sorted(pcpu_stats.keys())
# print(sorted(pcpu_stats.keys()))
