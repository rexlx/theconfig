from datetime import datetime

your_csv = 'data.csv'

# assigns days of the week a numeric key
day_dict = {
            'sunday': 0, 'monday': 1, 'tuesday': 2, 
            'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6}
datetime._DAYNAMES

# didnt actually need this, keeping for if we need inverse later
tframe_dict = {'0-4': 0, '5-9': 1, '10-14': 2, '15-19': 3, '20-23': 4}


def expand_data(day_dict):
    """
    opens a csv, gets the unix time from the first column
    and converts it to the day of the week and the hour
    (24 hour clock), print the unix time, the stat, the
    day of the week number, and the time frame number
    """
    with open(your_csv) as f:
        for line in f:
            x = line.split()
            # there is a comma linked to the unix time
            # 1543938517.1454322, take everything from
            # string except the last char (-1 in index
            unixtime = float(x[0][0:-2])
            # get the day of the week via datetime module
            day = datetime.fromtimestamp(unixtime).strftime("%A").lower()
            # and the hour (tframe is time frame)
            tframe = int(datetime.fromtimestamp(unixtime).strftime('%H'))
            # there might be a better way to do this
            # but it works. break the day down into groups
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
            # for formatting
            newline = "{} {}, {}, {}"
            # unix_time, metric, day number, time frame
            print(newline.format(x[0], x[1], d, tf))
            
    

    

expand_data(day_dict)
