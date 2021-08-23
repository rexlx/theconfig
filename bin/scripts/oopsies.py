import sys


def get_args():
    """
    gets args, not going to create an instance of argparser for just
    arg. if we plan to add options for header and delimiter control,
    then argparser will be used here instead.
    """
    if len(sys.argv) > 1:
        infile = sys.argv[1]
        return infile
    else:
        print("expected a file as an argument!")
        sys.exit(1)


def uniq_utime(infile):
    mydict = {}
    # open two files, read in the old, write out the new
    with open(infile, 'r') as f, open('new.csv', 'a') as new_file:
        # read in the first line (probably a header)
        header = f.readline()
        # if your csv doesnt have a header itll just write the first
        # line
        new_file.write(header)
        # read in everything else
        lines = f.readlines()
        for line in lines:
            # split the line by comma
            x = line.split(',')
            # dictionaries cant have multiples of keys, each unix time
            # is a unique key in the table, its value is the entire
            # line
            mydict[int(float(x[0]))] = line
            # for each key and value in the dictionary
        for k, v in sorted(mydict.items()):
            # print statement below is for debug
            # print(k)
            # write the line to the new file
            new_file.write(v)
        print('removed duplicate entries from ' + str(infile) +
              ' and created new.csv')


def main():
    infile = get_args()
    uniq_utime(infile)


if __name__ == '__main__':
    main()
