from datetime import datetime
import sys

"""
decription:

this script will covert unixtime into other types of data such as
weekday and timeframe. it takes a filename as an arg and expects a
float in the first column and for it to be a unix time stamp. the
amount of total columns shouldnt matter. it then appends each line with
a numerical representaion of the weekday and timeframe (see
dictionaries below to understand the mapping. this is mostly useful
when conducting tests accross the internet and you need to understand
what day and times are effecting traffic or i/o load

example:

python expand_utime.py cpu_speeds.csv

converts the line below
1544037826.95,1000,1000,1000,1000

to
1544037826.95,1000,1000,1000,1000,3,2
where 3 is wednesday and 2 means between 10am-2pm

it writes all data to a file named infile_oldextension.csv
cpu_speeds_csv.csv
"""

# assigns days of the week a number designator
day_dict = {'sunday': 0, 'monday': 1, 'tuesday': 2,
            'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6}

# didnt actually need this, keeping for if we need inverse later
tframe_dict = {'0-4': 0, '5-9': 1, '10-14': 2, '15-19': 3, '20-23': 4}


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


def expand_data(infile, day_dict):
    """
    opens a csv, gets the unix time from the first column and converts it to
    the day of the week and the hour (24 hour clock), print the unix time, the
    stat, the day of the week number, and the time frame number
    """
    modified_extension = infile.replace(".", "_")
    outfile = modified_extension + '.csv'
    with open(infile) as f, open(outfile, 'a') as newfile:
        header = f.readline()
        newfile.write(header)
        for line in f:
            x = line.split(',')
            # there is a comma linked to the unix time
            # 1543938517.1454322, take everything from string except the
            # last char (-1 in index
            try:
                unixtime = float(x[0])
                # get the day of the week via datetime module
                day = datetime.fromtimestamp(unixtime).strftime("%A").lower()
                # and the hour (tframe is time frame)
                tframe = int(datetime.fromtimestamp(unixtime).strftime('%H'))
                # there might be a better way to do this but it works.
                # break the day down into groups
                if tframe <= 4:
                    tf = 0
                elif tframe <= 9:
                    tf = 1
                elif tframe <= 14:
                    tf = 2
                elif tframe <= 19:
                    tf = 3
                else:
                    tf = 4
                # get the number for the weekday
                d = day_dict[day]
                # append the string with day, tframe
                if '\n' in x[-1]:
                    x[-1] = x[-1].strip('\n')
                x.extend([str(d), str(tf)])
                # #print(x)
                # theres probably a newline ch in there somewhere,remove
                if '\n' in x:
                    x.remove('\n')
                # join all the elements with a , between them
                newline = ','.join([e for e in x])
                newfile.write(newline + '\n')
            # the file likely has a string based header, this will throw
            # a value error, catch / skip it and get on with life
            except Exception as e:
                print(e, 'skipping')
                continue


def main():
    infile = get_args()
    expand_data(infile, day_dict)


if __name__ == "__main__":
    main()
