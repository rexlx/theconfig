import os
import argparse
import time
from six.moves import input as inp

"""
description:

this tool swaps a files extension. it will work recursively, or in one
directory.

example:

$ python extension_changer.py -h
usage: extension_changer.py [-h] [-p PATH] [-o OLD] [-n NEW] [-r]

This script converts file extensions

optional arguments:
  -h, --help  show this help message and exit
  -p PATH     path to dir
  -o OLD      old extension
  -n NEW      new extension
  -r          is recursive

python extension_changer.py -p /home/syseng/bin/data/examples/ -o exp -n txt
"""

# you can hard code values here if you dont want a bunch of args
user_path = './'
user_old = 'fake'
user_new = 'fake2'

changelog = './ext_change.log'


def get_args():
    """
    get the cli args via the argparse module
    """
    msg = "This script converts file extensions"
    # create an instance of parser with our unique msg
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-p', dest='path', required=False, help="path to dir")
    parser.add_argument('-o', dest='old', required=False, help="old extension")
    parser.add_argument('-n', dest='new', required=False, help="new extension")
    parser.add_argument('-u', dest='undo', required=False, action="store_true",
                        help="revert changes")
    parser.add_argument('-r', dest='recursive', required=False,
                        action="store_true", help="is recursive")
    args = parser.parse_args()
    if args.path:
        path = args.path
    else:
        path = user_path
    if args.old:
        old = args.old
    else:
        old = user_old
    if args.new:
        new = args.new
    else:
        new = user_new
    if args.undo:
        undo = True
    else:
        undo = False
    if args.recursive:
        recursive = True
    else:
        recursive = False
    return path, recursive, old, new, undo


def get_files(recursive, path):
    """
    returns a python list of files with full paths. requires two
    parameters: recursive (boolean) and path (string)
    """
    if not recursive:
        # this makes a list of just filenames (no paths)
        filenames = [e for e in os.listdir(path)]
        # but we wants full paths, use an os path join
        file_list = [os.path.join(path, e) for e in filenames]
    else:
        # this will decend into all subdirs
        file_list = [os.path.join(dir_path, x)
                     for dir_path, dirs, files in os.walk(path)
                     for x in files]
    return file_list


def handle_log():
    """
    handles removal / backup of the change log
    """
    # if the changelog is there and isn't empty
    if os.path.exists(changelog) and os.path.getsize(changelog) > 0:
        print("detected a changelog! if deleted you wont be able to revert!")
        # here we get the user input 'y/n/b'. some genius decided to
        # change the input method for python2/3 so you have to use a
        # compatibility module called six. look how i imported it up
        # top to see how this was achieved
        choice = inp("remove? y/n/b (yes/no/backup-and-remove)").lower()
        if choice == 'y':
            # try to remove the change log
            try:
                os.remove(changelog)
                # exception is likely file does not exist
            except Exception as _e:
                # whatever it is we dont care
                pass
        # else they want to keep the file as is
        elif choice == 'n':
            print("exiting...")
            exit()
        # else they want to back it up and remove
        elif choice == 'b':
            # get the unix time for the backup name
            mod = str(round(time.time()))
            # append the unix time to the changelog
            new_changelog = './ext_change' + mod + '.log'
            # rename it (should remove)
            os.rename(changelog, new_changelog)
            # inform the user of the backup log name
            print('created ' + new_changelog)
            # try to remove again for whatever reason
            try:
                os.remove(changelog)
                # exception is like file does not exist
            except Exception as _e:
                # whatever it is we dont care
                pass
            # otherwise they entered in an unsupported option
            else:
                print("that wasn't an option, exiting")
                exit()


def change_extension(path, file_list, old, new):
    """
    changes the file extension and logs the modification
    """
    handle_log()
    with open(changelog, 'a') as f:
        for i in file_list:
            # if the file ends with the old extension
            if i.endswith(old):
                # split the filename into ('name', '.ext')
                base = os.path.splitext(i)[0]
                # add the new extension to the base file name
                newfile = base + '.' + new
                # log the move
                f.write('moving ' + i + ' to ' + newfile + '\n')
                # do the move
                os.rename(i, newfile)


def revert():
    """
    using the changelog, reverts files to previous name
    """
    # if log exists and is not empty
    if os.path.exists(changelog) and os.path.getsize(changelog) > 0:
        with open(changelog) as f:
            manifest = f.readlines()
        for i in manifest:
            old = i.split()[3]
            new = i.split()[1]
            print('moving ' + old + ' to ' + new)
            os.rename(old, new)
    else:
        print("couldnt find the change log!!!")


def main():
    """
    times the duration of the runtime, gets user args, gets the file
    list, changes the extension, informs user upon completion
    """
    start = time.time()
    path, recursive, old, new, undo = get_args()
    # if it is an undo, exit afterwards
    if undo:
        revert()
        exit()
    file_list = get_files(recursive, path)
    change_extension(path, file_list, old, new)
    runtime = time.time() - start
    print('complete \nran for ' + str(runtime) + ' seconds.')


# if the scripts is being ran as itself, and not being imported
if __name__ == '__main__':
    # run
    main()
