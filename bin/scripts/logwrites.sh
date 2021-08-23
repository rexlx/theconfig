#!/bin/bash

x=$(date +"%F_%H-%M")
myfile=$x-writes.txt
/usr/bin/python /home/rxlx/bin/scripts/uptime.py > /home/rxlx/bin/data/$myfile
/usr/bin/python /home/rxlx/bin/scripts/total_rw.py \
>> /home/rxlx/bin/data/$myfile
