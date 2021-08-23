from __future__ import print_function
import multiprocessing as mp
import datetime as dt
import os, platform, sys, socket
try:
    import netifaces as ip
    netifaces = True
except ImportError:
    netifaces = False


def get_args():
    """
    gets arguments
    """
    # if user adds -v arg
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v':
            # they want the model. needs root priv
            verbose = True
        return verbose
    else:
        verbose = False
        return verbose


def get_dist():
    # this will not work on windows, assume linux
    dist = platform.platform()
    # #x = ' '.join(e for e in dist)
    print("Distribution".ljust(16) + dist)


def get_model():
    """
    this gets the model of the machine, requires superuser
    permissions. it is not on by default, and is invoked
    with the the -v option
    """
    try:
        # this leverages dmidecode command
        mdl = os.popen('dmidecode | grep "Product Name"')
        model = mdl.readline().split(': ')
        product = model[1]
        # #return product
        print('[model]')
        print('Model'.ljust(16) + product, end='')
    # exception should be premission denied, it is
    # possible perhaps ddmidecode command isnt
    # installed as well.
    except Exception as e:
        print("couldn't get_model(), you need higher permissions", e)


def get_uptime():
    """
    this function opens the uptime file and, using the
    seconds_to_readable() function, converts it to
    something more readable
    """
    with open('/proc/uptime', 'r') as f:
        for i in f:
            line = str(i).split()
            uptime = int(float(line[0]))
    # converted here
    runtime = str(dt.timedelta(seconds=uptime))
    print('Runtime'.ljust(16) + runtime)


def get_cpu():
    """
    this function opens the cpuinfo file and gets some
    info about the cpu :)
    """
    with open('/proc/cpuinfo') as f:
        # count the cpu cores with multiprocessing module
        # includes hyperthreaded cores
        total_cores = mp.cpu_count()
        # make some empty lists for later
        sock_count = []
        core_count = []
        for line in f:
            # matches physical id
            if 'cal id' in line:
                sock_count.append(line)
            # this will get the cpu name
            if 'model name' in line:
                mod = line.split()
                model = mod[3:]
                cpu_model = ' '.join(str(e) for e in model)
            # only counts real cores, not hyper threaded ones
            if 'cpu cores' in line:
                cores = line.split()
                core_count.append(cores[3])
    # convert to set to remove duplicates
    sockets = set(sock_count)
    # the amount of total real cores is the real core count
    # multiplied by the amount of sockets (cpus) on board
    real_cores = int(core_count[-1]) * int(len(sockets))
    print('\n[cpu]')
    print('CPU Model'.ljust(16) + cpu_model)
    print('Sockets'.ljust(16) + str(len(sockets)))
    print('Real Cores'.ljust(16) + str(real_cores))
    print('Total Cores'.ljust(16) + str(total_cores))


def get_mem():
    """
    opens meminfo, gets meminfo
    """
    with open('/proc/meminfo') as f:
        for line in f:
            # gets total memory
            if 'MemTotal' in line:
                total = line.split()
                mem_in_kb = total[1]
                # convert to GiB
                kb_to_gb = int(mem_in_kb) / (1024 ** 2.0)
                # we dont need many decimals, two will do
                mem_in_gb = "{0:.2f}".format(kb_to_gb)
    print('\n[memory]')
    print('Total Memory'.ljust(16) + mem_in_kb + ' (' + str(mem_in_gb)
          + 'gb)')


def get_net():
    """
    this is the preferred method of getting the network info. it
    leverages the netifaces module instead of opening a subprocess to
    run the linux ip command. netifaces is usually in the std library,
    but if it isnt, we will use another function
    """
    # ip is an alias for the netifaces module
    # create a list network devices
    devs = ip.interfaces()
    # and a list of gateways
    gws = ip.gateways()
    # get the default gw and iface
    dfaultgw = gws['default'][2][0]
    dfaultiface = gws['default'][2][1]
    # initialize an empty dictionary
    ipaddrs = {}
    # for item in the network devices list
    for i in devs:
        # get their address info
        all_addrs = ip.ifaddresses(i)
        # 2 is the default dictionary key in netifaces for 'AF_INET'
        # which is the address we're interested in
        if 2 in all_addrs:
            # append the ipaddrs dict with the device name as the key
            # and the address as the value. the ifaddresses from
            # netifaces returns the data in nested dictionaries, we
            # specify the key '2', the list index, 0, then the addr key
            ipaddrs[i] = all_addrs[2][0]['addr']
    # print out the data, unless it's loopback
    print('\n[network]')
    print("Gateway".ljust(16) + dfaultgw + " (via " + dfaultiface + ")")
    # pad = max(len(e) for e in ipaddrs.keys()) + 1
    for dev, addr in ipaddrs.items():
        if addr != '127.0.0.1':
            print(dev.ljust(16) + addr)


def get_net_from_ip():
    """
    get details about network state via the linux ip command. only used
    if the netifaces isn't in the python std lib
    """
    # get the hostname via socket module
    hostname = socket.gethostname()
    # ip command can be in different places, test for this
    if os.path.isfile('/usr/sbin/ip'):
        # run ip route, gives us good data
        f = os.popen('/usr/sbin/ip route')
        is_linux_with_ip = True
    elif os.path.isfile('/sbin/ip'):
        f = os.popen('/sbin/ip route')
        is_linux_with_ip = True
    else:
        # if no ip, its time to update your server
        print("Missing 'ip' package")
        is_linux_with_ip = False
    if is_linux_with_ip:
        for line in f:
            if 'default' in line:
                data = line.split()
                # get default gateway and interface
                gateway, dev = data[2], data[4]
    # get ip as socket sees it
    try:
        ipaddr = socket.gethostbyname(hostname)
    # however this doesnt always work on say lab machines
    except Exception as e:
        # although we want to avoid opening up subproceses, we're out
        # of options as far as i know
        cmd = '/usr/sbin/ip route get ' + gateway
        # get the route details of the default gateway
        iproute = os.popen(cmd)
        for i in iproute:
            # theres this stupid '\n  cache' string in the output, if
            # we see it, just continue on like it doesnt exist
            if 'cache' in i:
                continue
            # get the ipaddr
            data = i.split()
            ipaddr = data[4]
    print('\n[network]')
    print('IP'.ljust(16) + ipaddr)
    print('Gateway'.ljust(16) + gateway)
    print('Interface'.ljust(16) + dev)
    # = 'Hostname'.ljust(16) + hostname


def get_disks():
    """
    gets details about disk usage
    """
    # create an empty list for the filesystems
    fsystems = []
    fsystems.append('auto')
    with open("/proc/filesystems", "r") as f:
        for line in f:
            # we are only interested in lines that dont start with
            # 'nodev'
            if not line.startswith("nodev"):
                # add that to the phys_dev list.
                fsystems.append(line.strip())
    # create empty dictionary for partitions
    partitions = {}
    with open("/etc/fstab", "r") as f:
        for line in f:
            # in some cases there will be a none in there, we dont
            # want it
            if line.startswith('none'):
                continue
            try:
                fields = line.split()
                device = fields[0]
                mountpoint = fields[1]
                fstype = fields[2]
                # we only want stuff like ext4, xfs, ...etc
                if fstype not in fsystems:
                    continue
                # append the partitions dict with the device as the
                # key and the mountpoint and fstype as its values. we
                # dont really us fstype, but it may come in handy
                # EXAMPLE: '/dev/sdb': ['/home/rxlx/Mstor', 'ext4']
                partitions[device] = [mountpoint, fstype]
            except Exception as e:
                error = e
    # sometimes the partition names get very long, check its len
    mounts = []
    for i in partitions.values():
        mounts.append(i[0])
    pad = max(len(e) for e in mounts) + 1
    # # we want to keep our default 16 pad at the min
    if pad < 16:
        pad = 16
    print('\n[partitions]')
    # create/print a header
    print("name".ljust(pad) + "total".ljust(8) + "used".ljust(8)
          + "%".ljust(6))
    for part in partitions.keys():
        mount = partitions[part][0]
        # we dont care about boot devices
        if 'boot' in mount:
            continue
        # this is how we determine disk util, do a statvfs on the
        # mountpoint
        try:
            fs_data = os.statvfs(mount)
            # some basic math, note 1024 ** 3 turns bytes into GB
            free = round((fs_data.f_bavail * fs_data.f_frsize)
                         / (1024 ** 3), 2)
            total = round((fs_data.f_blocks * fs_data.f_frsize)
                          / (1024 ** 3), 2)
            used = round((fs_data.f_blocks - fs_data.f_bfree)
                         * fs_data.f_frsize / (1024 ** 3), 2)
            try:
                percent = round((used / total) * 100, 2)
            except ZeroDivisionError:
                # we dont want to destroy the universe, catch the zero div
                percent = 0
            # print(part[5:].ljust(pad) + str(total).ljust(8)
            #       + str(used).ljust(8) + str(percent).ljust(6))
        except OSError:
            free, total, used, percent = [None] * 4
            # print(part[5:].ljust(pad) + str(total).ljust(8)
            #       + str(used).ljust(8) + str(percent).ljust(6))
        finally:
            print(mount.ljust(pad) + str(total).ljust(8)
                  + str(used).ljust(8) + str(percent).ljust(6))


def main():
    """
    we finally made it.
    """
    # determine verbisity level from get_args
    verbose = get_args()
    # use the hostname as a title and center it in '-'
    print('\n' + socket.gethostname().center(80, '-'))
    if verbose:
        get_model()
    # leaving this commented in case someone
    # wants it on by defualt
    # #get_model()
    print('\n[system]')
    get_dist()
    get_uptime()
    get_cpu()
    get_mem()
    if netifaces:
        get_net()
    else:
        get_net_from_ip()
    get_disks()
    print('\n')


# if the script is being ran as itself and not imported
if __name__ == '__main__':
    main()
