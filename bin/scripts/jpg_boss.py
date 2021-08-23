#!/usr/bin/python3

from __future__ import print_function
import os, re, time, shutil, argparse, platform, calendar
import PIL.Image as img

# --USER--VARIABLES-- #
home = os.path.expanduser("~")
user_vdir = os.path.join(home, 'Mstor/Videos')
user_source = os.path.join(home, 'Downloads/NitroShare')
user_bdir = os.path.join(user_source, 'Mstor/Pictures/loose')
user_dest = os.path.join(home, 'Mstor/Pictures')
test_file = 'jpg_boss_dryrun.txt'
# --USER--VARIABLES-- #


def get_args():
    """
    gets cli args via the argparse module
    """
    msg = "This script organizes photos by year"
    # create an instance of parser from the argparse module
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-t', dest='test', required=False,
                        action="store_true",
                        help="dry run, output to log file")
    parser.add_argument('-s', dest='source', required=False, help="source dir")
    parser.add_argument('-d', dest='dest', required=False,
                        help="destination dir")
    parser.add_argument('-b', dest='bdir', required=False,
                        help="dir to store images without year data")
    parser.add_argument('-v', dest='vdir', required=False,
                        help="dir to store videos in")
    parser.add_argument('-l', dest='logfile', required=False)
    parser.add_argument('-n', dest='nomonth', required=False,
                        action="store_true",
                        help="do not make directories for months")
    parser.add_argument('-k', dest='keep_files', required=False,
                        action="store_true",
                        help="dont remove files from source dir")
    args = parser.parse_args()
    if args.test:
        test = True
    else:
        test = False
    if args.source:
        source = args.source
    else:
        source = user_source
    if args.dest:
        dest = args.dest
    else:
        dest = user_dest
    if args.bdir:
        bdir = args.bdir
    else:
        bdir = user_bdir
    if args.vdir:
        vdir = args.vdir
    else:
        vdir = user_vdir
    if args.logfile:
        logfile = args.logfile
    else:
        logfile = 'jpg_boss.log'
    if args.nomonth:
        nomonth = True
    else:
        nomonth = False
    if args.keep_files:
        keep_files = True
    else:
        keep_files = False
    return test, source, bdir, vdir, dest, logfile, nomonth, keep_files


def handle_logs(test_file, logfile):
    """
    removes the dry run log and error log
    """
    try:
        os.remove(test_file)
        os.remove(logfile)
    except Exception as e:
        # exception is likely file does not exist, we dont care
        error = e
        return error


def get_files(source):
    """
    utilizes the os module walk function to create
    a list of files recursively
    """
    # list comprehension the joins the direcctory
    # path and file name
    file_list = [os.path.join(dir_path, x)
                 for dir_path, dirs, files in os.walk(source)
                 for x in files]
    return file_list


def dir_checker(target):
    """
    receives target as parameter, if it exists, cool
    if not, make it and notify user
    """
    try:
        # create the path if it doesnt exist
        if not os.path.exists(target):
            os.makedirs(target)
            print('Created ' + str(target))
    except Exception as e:
        # likely exception is permission related, this should be run as
        # a regular user in a place they have access to.
        print(target, e)


def count_media(files):
    """
    will count files that match a certain extension
    """
    png = 0
    jpg = 0
    mp4 = 0
    other = []
    for i in files:
        if i.lower().endswith('jpg'):
            jpg += 1
        elif i.lower().endswith('png'):
            png += 1
        elif i.lower().endswith('mp4'):
            mp4 += 1
        else:
            # the file name and extension as per os splitext
            fname, fext = os.path.splitext(i)
            # append the other list
            other.append(fext)
    # create a set from the other list (essentially just a list of
    # unique extensions)
    others = set(other)
    msg = "found {} jpgs, {} pngs, {} mp4s, and the following other types:"
    print(msg.format(jpg, png, mp4))
    for i in others:
        # print the number of occurences of an extension, then the ext
        # we end with " " instead of newline to keep the output a
        # little neater. **NOTE**, we have to import the print_function
        # from the future for this to work in python2!
        print(other.count(i), i, end=" ")
    print('\n')


def move_mp4s(files, vdir, test, keep_files):
    """
    looks for mp4s and moves them to a target dir. currently, this
    assumes the date is in the title of the mp4, but this obviously
    wont always be the case, i intend to add metadata support for mp4s
    ...if it exists
    """
    for i in files:
        if i.endswith('mp4'):
            # use re to match a year in the movie name
            match = re.search(r'20\d\d', i)
            if match:
                # if it matches, build the target location
                target = os.path.join(vdir, match.group(0))
                # get the the file with no path
                thefile = os.path.basename(i)
                # concat that to the target path to get our new file
                video = os.path.join(target, thefile)
                # see if the target dir already exists or make it
                # if user is doing a dry run
                if test:
                    with open(test_file, 'a') as tfile:
                        if os.path.isfile(video):
                            tfile.write(video + ' already exists!\n')
                        else:
                            tfile.write('moving ' + i + ' to ' + target + '\n')
                else:
                    dir_checker(target)
                    print('moving ' + i + ' to ' + target)
                    # move and remove
                    shutil.copy2(i, target)
                    if not keep_files:
                        os.remove(i)


def move_by_data(files, test, dest, bdir, logfile, nomonth, keep_files):
    """
    if the file is a jpg, attempt to view exif data and get the date
    move and remove to target dir. writes exceptions to a log file
    ./jpg_boss.log
    """
    # get the OS
    operating_system = platform.platform().lower().split('-')[0]
    months = {k: v for k, v in enumerate(calendar.month_abbr)}
    for i in files:
        if i.lower().endswith('jpg'):
            # if its a jpg, open it. This should not decode
            try:
                pic = img.open(i)
                # get the exif data or its None
                pic_meta_data = pic._getexif()
                if operating_system == 'windows':
                    pic.fp.close()
            except Exception as e:
                print(e)
            if pic_meta_data is None:
                # no exif data, it goes to the bastard_dir (bdir)
                target = bdir
            try:
                # try to get the date out of the exif data
                date = pic_meta_data[306]
                # date is in this format: '2016:09:27 17:48:17'
                year = date[0:4]
                pdate = year
                if not nomonth:
                    month_int = int(date[5:7])
                    month = months[month_int]
                    pdate = os.path.join(year, month)
                # build the target location
                target = os.path.join(dest, pdate)
            except Exception as e:
                # write exceptions to log file
                with open(logfile, 'a') as f:
                    f.write(str(e) + '\n')
            # check the dir state
            # extract just the file from the src oath
            thefile = os.path.basename(i)
            # add that file name to the target dir
            photo = os.path.join(target, thefile)
            # if user is doing a dry run
            if test:
                # record what the script will do
                with open(test_file, 'a') as tfile:
                    try:
                        if os.path.isfile(photo):
                            tfile.write(photo + ' already exists!\n')
                    except Exception as e:
                        print(photo, e)
                    else:
                        tfile.write('moving ' + i + ' to ' + target + '\n')
            else:
                dir_checker(target)
                # if the file exists, do nothing
                try:
                    if os.path.isfile(photo):
                        print('file already exists!')
                except Exception as e:
                    print(photo, e)
                else:
                    # move and remove
                    shutil.copy2(i, target)
                    if not keep_files:
                        os.remove(i)
    if test:
        # tell the user where the dry run results are
        print('dry run results in: ' + test_file)


def main():
    # mark the start time
    start = time.time()
    # get the args
    test, source, bdir, vdir, dest, logfile, nomonth, keep_files = get_args()
    # get the file list
    files = get_files(source)
    # handle the dry run log
    handle_logs(test_file, logfile)
    # move jpgs
    move_by_data(files, test, dest, bdir, logfile, nomonth, keep_files)
    # move mp4s
    move_mp4s(files, vdir, test, keep_files)
    # count file extensions
    count_media(files)
    # script is done, mark the time
    end = time.time()
    length = end - start
    # tell them how long it took
    print('took ' + str(round(length, 2)) + ' seconds')


# if the file is being ran as itself and not being imported
if __name__ == '__main__':
    main()
