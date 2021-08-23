import os, time
from shutil import copyfile
import regular tools as rtk


def gen_file(name, limit, step):
    test_file = name
    start = time.time()
    with open(test_file, 'a') as f:
        file_size = os.stat(test_file)
        f_size = file_size.st_size
        while f_size < limit:
            test_file.write(os.urandom(step))
    now = time.time()
    length = now- start
    return length

def mv_file(src, dst):
    start = time.time()
    copyfile(src, dst)
    now = time.time()
    length = now- start
    return length


