from __future__ import print_function
import os

serial = os.popen("/usr/bin/cpuid | grep 'number:' | uniq | awk -F ':' '{ print $2 }'")
hostname = os.popen('hostname')
server = hostname.readline().strip()

for line in serial:
    data = line.split('-')

formatted_data = ''.join(str(e) for e in data)
cpuid = formatted_data[4:9]
print(server.ljust(30) + cpuid)

