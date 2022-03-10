import os
import socket
import getpass
import uptime as up


def get_info():
    uname = getpass.getuser()
    hostname = socket.gethostname()
    # wd = os.path.dirname(os.path.realpath(__file__))
    wd = os.getcwd()
    with open('/proc/uptime', 'r') as f:
        elapsed_time = f.readline().split()[0]
    u = up.time_in_seconds(elapsed_time)
    msg = f"user: {uname}\nhostname: {hostname}\nworkdir: {wd}\nuptime:\n{u}"
    print(msg)


if __name__ == "__main__":
    get_info()