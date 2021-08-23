import os
import argparse
import random
import shutil


def get_args():
    """
    gets cli args via the argparse module
    """
    msg = """This tool gets the size of a directory and displays info about the
contents"""
    # create an instance of parser from the argparse module
    parser = argparse.ArgumentParser(description=msg)
    # add expected arguments
    parser.add_argument('-s', dest='source', required=False, help="source dir")
    parser.add_argument('-d', dest='dest', required=False, help="dest dir")
    args = parser.parse_args()
    if args.source:
        source = args.source
    else:
        print("got no source dir")
        exit()
    if args.dest:
        dest = args.dest
    else:
        print("got no dest dir")
        exit()
    return source, dest


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


def randomize_mp3s(src, dst):
    for i in src:
        choice = random.choice(src)
        src.remove(choice)
        if choice.lower().endswith("mp3"):
            _file_ = os.path.basename(i)
            target = os.path.join(dst, _file_)
            shutil.copy2(choice, target)

def main():
    # get the args
    source, dst = get_args()
    # get the file list
    files = get_files(source)
    randomize_mp3s(files, dst)


if __name__ == "__main__":
    main()
