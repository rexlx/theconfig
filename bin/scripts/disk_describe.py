from __future__ import division
import os
import sys

my_path = '/sys/block/'


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
    converted_data = str(formated_data).rjust(7) + symbol
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


def get_dsize(hard_drive):
    # hdds = get_disks()
    # for disk_name in hdds:
    target = my_path + hard_drive + '/size'
    try:
        with open(target) as f:
            dsize = int(f.readline().strip())
        return dsize
    except IOError:
        print('\ncould not open ' + target)
        sys.exit(1)


def free_space(hard_drive):
    fs_data = os.statvfs('.')
    available = fs_data.f_bavail
    frsize = fs_data.f_frsize
    free_space = available * frsize
    return free_space


def main():
    disks = {}
    hdds = get_disks()
    pad = max(len(e) for e in hdds)
    for disk_name in hdds:
        bsize = get_block_size(disk_name)
        dsize = get_dsize(disk_name)
        disk_size = dsize * bsize
        free = free_space(disk_name)
        used = disk_size - free
        # print(bsize, dsize, disk_size, free, used)
        disk_usage = make_readable(used)
        total = make_readable(disk_size)
        print(disk_name.ljust(pad) + ' : ' + str(total))


if __name__ == '__main__':
    main()
