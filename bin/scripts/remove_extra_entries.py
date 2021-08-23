import sys, os

f_name = sys.argv[1]
out_file = 'no_extras_' + f_name

data = set(line.strip() for line in open(f_name))


try:
    os.remove(out_file)
except OSError:
    pass

with open(out_file, 'a') as f:
    for i in data:
        f.write(i + '\n')

