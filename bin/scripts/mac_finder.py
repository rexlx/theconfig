#!/usr/bin/python
from __future__ import division
import os, sys, csv, time

start_time = time.time()

# where the file repos are
my_path = '/home/'
# the name of the tsung csv, copy yours to 'macs' or change this
tsung_csv = '/home/macs'
# list for expected macs (gets filled in later)
expected_macs = []

# if the csv exists
try:
    # open the file and extract the macs
    with open(tsung_csv, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            expected_macs.append(row[4])
# if the csv isn't there
except IOError:
    # nothing to compare, dont waste time scanning dirs, exit.
    print("expected a tsung csv named 'macs'")
    sys.exit(1)

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
    converted_data = str(formated_data).ljust(6) + symbol
    return converted_data

# creates a list of file names that match 'aaa' recursively
# this is what takes the most time
ps_files = [os.path.join(x[0:12])
            for dir_path, dirs, files in os.walk(my_path)
            for x in files if "aaa" in x]

# count the total files & space taken
matches = len(ps_files)
# x is the total files * the file size in bytes (from ls -ltr)
x = matches * 266650
# convert to human readable
size = make_readable(x)
print("\nFound " + str(matches) + " files: " + size)

# create two sets for comparrison
macs_on_ps = set(ps_files) 
macs_from_csv = set(expected_macs)
# tests whether every element in macs_from_csv is in macs_on_ps
if macs_from_csv <= macs_on_ps:
    # all expected macs are on the system
    print("all expected macs located on system\n")
else:
    # there is a difference between the sets
    print("difference detected, getting macs...\n") 
    # create a list from the files not on the ps and print them
    missing_macs = list(macs_from_csv - macs_on_ps)
    try:
        os.remove('/home/missing_macs.txt')
    except OSError:
        pass
    with open('/home/missing_macs.txt', 'a') as fname:
        for m in missing_macs:
            fname.write(m + '\n')
    print('missing macs dumped into /home/missing_macs.txt')

now = time.time()
runtime = now - start_time
print("\ncomplete, test took "+ str(runtime) + " seconds")
