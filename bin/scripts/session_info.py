import os
import socket
import getpass
import uptime as up


def get_info():
    """get_info() gets information about the users session and returns
    either an error message (if there was an error), or a summary of
    the session

    Returns:
        string: multiline string inside a reurn block, or an error
    """

    # attempt to open the uptime file (linux only)
    try:
        with open('/proc/uptime', 'r') as f:
            # create a list of the first line and specify we want the
            # first [0] element, which is uptime in seconds.
            elapsed_time = f.readline().split()[0]
    except Exception as err:
        return f"got on error:\t {err}\nexiting..."

    # converted value for seconds to human readable
    u = up.time_in_seconds(elapsed_time)
    # get the user name and hostname
    uname = getpass.getuser()
    hostname = socket.gethostname()
    # in the event a directory was deleted, we may get a FileNotFound
    # error, handle it.
    try:
        wd = os.getcwd()
    except FileNotFoundError as err:
        return (
                f"it appears the directory {wd} does not exist\n"
                f"The directory may have been deleted...\n"
        )

    return (
        f"hostname: {hostname}\n"
        f"user:     {uname}\n"
        f"workdir:  {wd}\n"
        f"uptime:   {u}"
    )


# if this script is being ran as itself (and not imported), run get_info
# which is effectively our "main" function.
if __name__ == "__main__":
    print("_" * 34)
    print(get_info())
