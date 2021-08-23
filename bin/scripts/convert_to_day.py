from datetime import datetime
import sys

def convert_to_day(unixtime):
    day = datetime.fromtimestamp(unixtime).strftime("%A")
    return day


output = convert_to_day(float(sys.argv[1]))
print(output)
