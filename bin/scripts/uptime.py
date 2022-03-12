import sys
import socket

def time_in_seconds(seconds):
    """
    A python program that converts seconds to
    human readable times
    """
    #Copies the number
    s = int(float(seconds))

    #Sets default values
    day = 0
    hour = 0
    mins = 0

    # this loop tests the input and breaks
    # it into years, months, weeks, days,
    # hours, and seconds
    while True:
        if s < 0:
            print("thats less then zero...")
            error = 'true'
            break
        elif s >= 86400:
            s -= 86400
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
    formated_time = f"{day:>4}d {hour:>4}h {mins:>4}m {s:>4}s"
    return formated_time


def main():
    with open('/proc/uptime', 'r') as f:
        elapsed_time = f.readline().split()[0]
    print(f"{socket.gethostname():<25}{time_in_seconds(elapsed_time)}")


if __name__ == "__main__":
    main()
