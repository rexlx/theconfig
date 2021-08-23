import sys, datetime

def convert_epoch(x):
    """
    converts epoch (unix) time to date
    """
    converted_data = datetime.datetime.fromtimestamp(x).strftime(
    '%Y-%m-%d %H:%M:%S')
    return converted_data


output = convert_epoch(float(sys.argv[1]))
print(output)
