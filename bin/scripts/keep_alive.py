import sys, time

start_time = time.time()
refresh = 20

def sec(seconds):
    """
    A python program that converts seconds to
    human readable times
    """
    #Copies the number
    s = int(seconds)

    #Sets default values
    year = 0
    month = 0
    week = 0
    day = 0
    hour = 0
    mins = 0

    # this loop tests the input and breaks
    # it into years, months, weeks, days,
    # hours, and seconds
    while True:
        if s < 0:
            print("sorry thats less than zero")
            break
        elif s >= 31556952:
            s -= 31556952
            year += 1
            continue
        elif s >= 2628000:
            s -= 2628000
            month += 1
            continue
        elif s >= 603120:
            s -= 603120
            week += 1
            continue
        elif s >= 86160:
            s -= 86160
            day += 1
            continue
        elif s >= 3600:
            s -= 3600
            hour += 1
            continue
        elif s >= 60:
            s -= 60
            mins += 1
            continue
        elif s < 60:
            break
    converted_data = str(year) + "y " + str(week) + "w " + str(day) \
                     + "d " + str(hour) + "h " + str(mins) + "m " \
                     + str(s) + "s"
    return converted_data


def show_runtime(human_time):
    msg = 'running: ' + str(human_time) + ' '
    sys.stdout.write('%s\r' % msg)
    sys.stdout.flush()

def get_args():
    if len(sys.argv) > 1:
        runtime = sys.argv[1]
        return runtime
    else:
        runtime = 'infinity'
        return runtime

def main(_runtime):
    if _runtime == 'infinity':
        while True:
            now = time.time()
            uptime = now - start_time
            human_time = sec(uptime)
            show_runtime(human_time)
            time.sleep(refresh)
    else:
        runtime = int(_runtime)
        uptime = 0
        while uptime <= runtime:
            now = time.time()
            uptime = now - start_time
            human_time = sec(uptime)
            show_runtime(human_time)
            time.sleep(refresh)

if __name__ == '__main__':
    runtime = get_args()
    main(runtime)
    print('\n')
