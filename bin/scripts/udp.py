import socket
import struct
import time

# using named indexes to keep code readable
local_addr = 1
rem_addr = 2
tx_q = 4
rx_q = 5
_drops_ = 14

def convert2ip(val):
    # the value is in hexadecimal, convert to int
    data = int(val, 16)
    # we use socket to convert packed binary to IP string, struct
    # creates the pack with < meaning litte-endian and L meaning
    # unsigned long
    ip = socket.inet_ntoa(struct.pack("<L", data))
    # return as str since we want to write to file later
    return str(ip)

def convert2int(val):
    # convert hexadecimal to int
    data = int(val, 16)
    return str(data)

def get_fields():
    # open the proc file
    with open("/proc/net/udp") as f:
        # dont care about the header
        header = f.readline()
        # get the data
        data = f.read()
    # create list of lists (there are several lines in the file)
    fields = [e.split() for e in data.split('\n')]
    return fields

def write_csv(line):
    # writes the csv
    with open("udp_drops.csv", "a") as f:
        f.write(line)

def poll():
    # get the fields list
    fields = get_fields()
    # for each line in the file
    for i in fields:
        try:
            # if the drops are none, dont continue
            if i[_drops_] == 0:
                continue
            # else drops are present
            # split the local and remote addrs by addr and port
            l_adr, l_prt = i[local_addr].split(":")
            l_adr = convert2ip(l_adr)
            l_prt = convert2int(l_prt)
            r_adr, r_prt = i[rem_addr].split(":")
            r_adr = convert2ip(r_adr)
            r_prt = convert2int(r_prt)
            # this is transmit queue
            t_q = str(i[tx_q])
            r_q = str(i[rx_q])
            drops = str(i[_drops_])
            # build our csv line
            line = "{},{},{},{},{},{},{},{}\n".format(
                                                      str(time.time()),
                                                      l_adr,
                                                      l_prt,
                                                      r_adr,
                                                      r_prt,
                                                      t_q,
                                                      r_q,
                                                      drops
                                                   )
            # write it
            write_csv(line)
        except Exception as e:
            # exception is likely a empty spot in array
            # print("encountered an exception, continuing\n{}".format(e))
            continue


def main():
    while True:
        poll()
        time.sleep(5)


if __name__ == "__main__":
    main()