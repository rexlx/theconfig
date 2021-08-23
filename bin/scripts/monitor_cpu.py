from __future__ import print_function
import time, psutil, datetime, sys

def one_min_poll():
    """
    this function gathers the cpu usage and frequency
    """
    one_min_load = []
    speeds = []
    count = 0
    # while the runtime is less than a minute
    while count <= 3:
        # get the cpu usage
        x = psutil.cpu_percent(interval=None, percpu=False)
        # add it to the load list
        one_min_load.append(x)
        # get the cpu speed
        freq = psutil.cpu_freq()
        # i only care about the current speed
        cpu_speed = freq.current
        # append the speeds list
        speeds.append(cpu_speed)
        # wait a second and increment. repeat.
        time.sleep(1)
        count += 1
    # determine the average usage for that minute
    one_min_avg = sum(one_min_load) / len(one_min_load)
    # determine low / high speed for poll period
    min_speed, max_speed = min(speeds), max(speeds)
    # dump the data into a csv file where the first column is cpu util
    # and the second is the current cpu speed
    #with open('cpuutil.plot', 'a') as loadfile:
        #for i in range(0, len(one_min_load)):
            #loadfile.write(str(one_min_load[i]) + ', ' + str(speeds[i]) + '\n')
    # return the average for that minute
    # return some values
    return one_min_avg, min_speed, max_speed

# this is a simple example of how to collect data
# for a certain period of time (480 minutes = 8 hours)
run_time = 0
while run_time < 2880:
    load, min_freq, max_freq = one_min_poll()
    data = "average usage: " + str(round(load, 2)) + " cpu speed min/max: " +\
    str(round(min_freq, 2)) + '/' + str(round(max_freq, 2))
    sys.stdout.write('%s\r' % data)
    sys.stdout.flush()
    run_time += 1
