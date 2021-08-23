from __future__ import print_function
import os, time, shutil, argparse, sys

# --USER--VARIABLES-- #
home = os.path.expanduser("~")
user_vdir = os.path.join(home, 'Videos')
user_source = os.path.join(home, 'Pictures')
user_bdir = os.path.join(user_source, 'loose')
user_dest = os.path.join(user_source, 'Phone')
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
    parser.add_argument('-r', dest='del_files', required=False,
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
    if args.del_files:
        del_files = True
    else:
        del_files = False
    return test, source, bdir, vdir, dest, logfile, nomonth, del_files


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
            # print('Created ' + str(target))
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
    exts = []
    for i in files:
        # the file name and extension as per os splitext
        fname, fext = os.path.splitext(i)
        # append the other list
        exts.append(fext)
    # create a set from the other list (essentially just a list of
    # unique extensions)
    extensions = set(exts)
    msg = "found the following extensions:"
    print(msg.format(jpg, png, mp4))
    for i in extensions:
        # print the number of occurences of an extension, then the ext
        # we end with " " instead of newline to keep the output a
        # little neater. **NOTE**, we have to import the print_function
        # from the future for this to work in python2!
        print(exts.count(i), i, end=" ")
    print('\n')


def mirror(files, test, src, dest, logfile, del_files):
    """
    """
    # get the OS
    # operating_system = platform.platform().lower().split('-')[0]
    file_count = len(files)
    pos = 1
    for i in files:
        msg = 'starting {} of {}'.format(pos, file_count)
        sys.stdout.write('%s\r' % msg)
        sys.stdout.flush()
        # thefile = os.path.basename(i)
        # print(i, src, dest)
        d = os.path.dirname(i)
        dir = d.replace(src, '')
        path = i.replace(src, '')
        # source_target = os.path.join(src, i)
        # dest_target = os.path.join(dest, path)
        dest_target = dest + path
        # if user is doing a dry run
        if test:
            # record what the script will do
            with open(test_file, 'a') as tfile:
                try:
                    if os.path.isfile(dest_target):
                        tfile.write(dest_target + ' already exists!\n')
                except Exception as e:
                    print(i, e)
                else:
                    tfile.write('moving ' + i + ' to ' + dest_target + '\n')
        else:
            dir_checker(dest + dir)
            # if the file exists, do nothing
            try:
                if os.path.isfile(dest_target):
                    print('file already exists!')
            except Exception as e:
                print(dest_target, e)
            else:
                # move and remove
                try:
                    shutil.copy2(i, dest_target)
                    if del_files:
                        os.remove(i)
                except Exception as e:
                    with open(logfile, 'a') as f:
                        f.write(str(e) + '\n')
        pos += 1
    if test:
        # tell the user where the dry run results are
        print('dry run results in: ' + test_file)


def main():
    # mark the start time
    start = time.time()
    # get the args
    test, source, bdir, vdir, dest, logfile, nomonth, del_files = get_args()
    handle_logs(test_file, logfile)
    # get the file list
    files = get_files(source)
    mirror(files, test, source, dest, logfile, del_files)
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
