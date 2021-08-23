
def get_mem():
    with open('/proc/meminfo') as f:
        for line in f:
            if 'MemAvailable' in line:
                total = line.split()
                mem_in_kb = total[1]
                kb_to_gb = int(mem_in_kb) / (1024 ** 2.0)
                mem_in_gb = "{0:.2f}".format(kb_to_gb)
    print('Free Memory'.ljust(14) + mem_in_kb + ' (' + str(mem_in_gb) \
          + 'gb)')
get_mem()
