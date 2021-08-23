#!/usr/bin/python
from __future__ import division
import os
import sys

"""
This script shows the total amount read / written to disk since startup

example output:

written:
dm-1            796.00 KB
nvme0n1         2.37   GB
nvme0n1p1       2.37   GB
sdb1            0.00   B
sdb             0.00   B
dm-2            3.31   GB
dm-0            8.34   GB
sdc3            11.32  GB
sdc1            4.50   KB
sdc             11.32  GB
sdc2            36.00  KB
sda1            7.24   MB
sda             7.24   MB

read:
dm-1            3.46   MB
nvme0n1         8.89   GB
nvme0n1p1       8.89   GB
sdb1            175.53 MB
sdb             177.71 MB
dm-2            607.03 MB
dm-0            2.00   GB
sdc3            2.60   GB
sdc1            4.86   MB
sdc             2.61   GB
sdc2            4.42   MB
sda1            69.86  MB
sda             72.04  MB
"""


def make_readable(val):
    """
    a function that converts bytes to human readable form.
    returns a string like: 42.31 TB
    example:
    your_variable_name = make_readable(value_in_bytes)
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
    converted_data = str(formated_data).ljust(6) + symbol
    return converted_data


def get_disks():
    """
    this function gets a list of reported block devices.
    returns a list of block devices as strings
    example:
    your_list_name = get_disks()
    """
    hard_disks = []
    # where the block device's dirs are
    my_path = '/sys/block/'
    # unpack an os walk
    for dir_path, dirs, files in os.walk(my_path):
        # we only care about the dirs value
        for i in dirs:
            # append the list of block devices to be returned
            hard_disks.append(i)
    return hard_disks


def get_block_size(hard_drive):
    """
    this function gets the sector size of a block device (usually 512 bytes).
    it requires a block device as a parameter.
    returns an integer
    example:
    your_var_name = get_block_size(disk_name)
    """
    my_path = '/sys/block/'
    # creates the full path the file containing block size
    target = my_path + hard_drive + '/queue/logical_block_size'
    # if the path above exists and can be opened as a file
    try:
        with open(target) as f:
            # get the block size
            b_size = int(f.readline().strip())
    # otherwise something terrible has happened, exit with 1
    except IOError:
        print('\ncould not open ' + target)
        sys.exit(1)
    return b_size


def get_written():
    """
    this function gets the total secotrs written since startup per partition
    and multiplies it by the sector size in bytes.
    """
    # creates empty dictionary to work with
    disks = {}
    # try and open the diskstats file
    try:
        with open('/proc/diskstats', 'r') as f:
            # for each line in the file, split it into columns
            for line in f:
                # unpack the columns (starts at 0)
                name, amount = line.split()[2], line.split()[9]
                # append the dictionary, partition
                disks[name] = amount
                can_move_on = True
    except IOError:
        print("\ncould not find '/proc/diskstats'!")
        can_move_on = False

    if can_move_on:
        hdds = get_disks()
        print('\nwritten:')
        for disk_name in hdds:
            for partition, value in disks.items():
                if disk_name in partition:
                    sector_size = int(get_block_size(disk_name))
                    amount_written = int(value) * sector_size
                    total_written = make_readable(amount_written)
                    print(partition.ljust(16) + total_written)


def get_read():
    """
    this function gets the total secotrs written since startup per partition
    and multiplies it by the sector size in bytes.
    """
    disks = {}
    try:
        with open('/proc/diskstats', 'r') as f:
            for line in f:
                name, amount = line.split()[2], line.split()[5]
                disks[name] = amount
                can_move_on = True
    except IOError:
        print("\ncould not find '/proc/diskstats'!")
        can_move_on = False

    if can_move_on:
        hdds = get_disks()
        print('\nread:')
        for disk_name in hdds:
            for partition, value in disks.items():
                if disk_name in partition:
                    sector_size = int(get_block_size(disk_name))
                    amount_read = int(value) * sector_size
                    total_read = make_readable(amount_read)
                    print(partition.ljust(16) + total_read)


get_written()
get_read()
