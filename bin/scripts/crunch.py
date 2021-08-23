import pyshark as ps
import sys
import pickle
import os
from collections import defaultdict

_file_ = sys.argv[1]
p_file = "cached_" + _file_
target6 = ""
target4 = ""


def make_readable(val):
    """
    a function that converts bytes to human readable form, returns a
    string like: 42.31 TB
    """
    data = float(val)
    tib = 1024 ** 4
    gib = 1024 ** 3
    mib = 1024 ** 2
    kib = 1024
    if data >= tib:
        symbol = ' TB'
        new_data = data / tib
    elif data >= gib:
        symbol = ' GB'
        new_data = data / gib
    elif data >= mib:
        symbol = ' MB'
        new_data = data / mib
    elif data >= kib:
        symbol = ' KB'
        new_data = data / kib
    else:
        symbol = ' B'
        new_data = data
    # we only care about two decimal places
    formated_data = "{0:.2f}".format(new_data)
    converted_data = str(formated_data).rjust(6) + symbol
    return converted_data


def cache_pcap(_file_):
    cap = ps.FileCapture(_file_, only_summaries=True,
                         decode_as={'udp.port==8001': 'snmp'})
    if not os.path.exists(p_file):
        all_stats = []
        all_sizes = []
        stats = defaultdict(list)
        sizes = defaultdict(list)
        for p in cap:
            if p.destination.startswith('f') or p.source.startswith('f'):
                continue
            key_string = p.source + ' > ' + p.destination
            stats[key_string].append(p.protocol)
            sizes[key_string].append(int(p.length))
            all_stats.append(p.protocol)
            all_sizes.append(int(p.length))
            # full_list[p.source].append(p.destination)
        # pickle.dump(stats, open(p_file, 'wb'))
        with open(p_file, 'wb') as f:
            pickle.dump([stats, all_stats, sizes, all_sizes], f)
        # pickle.dump(full_list, open(p_file, 'wb'))


def get_pads(_list_):
    addrs = []
    sizes = []
    pkts = []
    protos = []
    for i in _list_:
        addrs.append(i[0])
        sizes.append(i[1])
        pkts.append(i[2])
        protos.append(i[3])
    addr_pad = max(len(e) for e in addrs) + 1
    size_pad = max(len(str(e)) for e in sizes) + 1
    pkt_pad = max(len(str(e)) for e in pkts) + 1
    pad = max(len(e) for e in protos) + 1
    return addr_pad, size_pad, pkt_pad, pad


def count_occurences(_list_):
    packets = len(_list_)
    uniq_vals = set(_list_)
    # max_len = max(len(e) for e in uniq_vals) + 1
    msg = [e + ': ' + str(_list_.count(e)) for e in sorted(uniq_vals)]
    protocols = ' '.join(msg)
    return protocols, packets


def get_ipv6(stats, all_stats, sizes, all_sizes):
    lines = []
    # pad = max(len(e) for e in stats.keys()) + 1
    for k, v in stats.items():
        if ':' in k:
            packet_sizes = sizes[k]
            data = sum(packet_sizes)
            if data < 0:
                data = 0
            size = make_readable(data)
            protocols, packets = count_occurences(v)
            # print(k.ljust(pad) + ' | ' + size.ljust(9) + ' | ' + str(packets)
            #       + ' | ' + protocols)
            line = [k, size, packets, protocols]
            lines.append(line)
    addr_pad, size_pad, pkt_pad, pad = get_pads(lines)
    c = 1
    header = ("\naddress".ljust(addr_pad + 4) + "size".ljust(size_pad + 4)
              + "pkts".ljust(pkt_pad + 4) + "summary")
    print(header + '\n' + '-' * len(header))
    for i in lines:
        if c % 25 == 0:
            print(header + '\n' + '-' * len(header))
        print(i[0].ljust(addr_pad) + ' | ' + i[1].rjust(size_pad) + ' | ' +
              str(i[2]).ljust(pkt_pad) + ' | ' + i[3])
        c += 1


def get_ipv4(stats, all_stats, sizes, all_sizes):
    lines = []
    # pad = max(len(e) for e in stats.keys()) + 1
    for k, v in stats.items():
        if '.' in k:
            packet_sizes = sizes[k]
            data = sum(packet_sizes)
            if data < 0:
                data = 0
            size = make_readable(data)
            protocols, packets = count_occurences(v)
            line = [k, size, packets, protocols]
            lines.append(line)
    addr_pad, size_pad, pkt_pad, pad = get_pads(lines)
    c = 1
    header = ("\naddress".ljust(addr_pad + 4) + "size".ljust(size_pad + 4)
              + "pkts".ljust(pkt_pad + 4) + "summary")
    print(header + '\n' + '-' * len(header))
    for i in lines:
        if c % 25 == 0:
            print(header + '\n' + '-' * len(header))
        print(i[0].ljust(addr_pad) + ' | ' + i[1].ljust(size_pad) + ' | ' +
              str(i[2]).ljust(pkt_pad) + ' | ' + i[3])
        c += 1


def general_stats(stats, all_stats, sizes, all_sizes):
    all_proto, all_packets = count_occurences(all_stats)
    all_bytes = sum(all_sizes)
    print('\ntotal packets:\n' + str(all_packets))
    print('protocol stats:\n' + all_proto)
    total_size = make_readable(all_bytes)
    print('total size: ' + total_size)


def main():
    cache_pcap(_file_)
    # stats = pickle.load(open(p_file, 'rb'))
    with open(p_file, 'rb') as f:
        stats, all_stats, sizes, all_sizes = pickle.load(f)
    get_ipv6(stats, all_stats, sizes, all_sizes)
    get_ipv4(stats, all_stats, sizes, all_sizes)
    general_stats(stats, all_stats, sizes, all_sizes)


if __name__ == '__main__':
    main()
