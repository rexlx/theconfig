import time, argparse
import datetime as dt

def convert_date(x):
    """
    converts date to unix time
    """
    converted_data = time.mktime(x.timetuple())
    return converted_data


#output = convert_epoch(float(sys.argv[1]))
#print(output)
def main():
    msg = "converts dates to unix time"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument('date', nargs='+', type=int,
                        help="2019 08 31 23 59 59")
    args = parser.parse_args()
    if args.date:
        data = dt.datetime(*args.date)
        unixtime = convert_date(data)
        print(unixtime)

if __name__ == '__main__':
    main()
