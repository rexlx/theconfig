import os
import socket
import getpass
import uptime as up


def get_info():
    uname = getpass.getuser()
    hostname = socket.gethostname()
    wd = os.getcwd()
    with open('/proc/uptime', 'r') as f:
        elapsed_time = f.readline().split()[0]
    u = up.time_in_seconds(elapsed_time)
    return (
        f"hostname: {hostname}\n"
        f"user:     {uname}\n"
        f"workdir:  {wd}\n"
        f"uptime:   {u}"
    )


if __name__ == "__main__":
    print(get_info())
