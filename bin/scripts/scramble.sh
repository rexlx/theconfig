#!/bin/bash

#set -x

NAV=/home/rexreedfitzhugh
TARGET=/var/www/html/guest

randomize () {
	cat /dev/urandom | env LC_CTYPE=C tr -cd 'a-f0-9' | head -c 32
}

while [ true ]; do
sudo rm -rf $TARGET/*.tar || echo "nothhing at target location"
C=1
for orig in $NAV/guest/*;
do
	real[$C]=$orig
	C=$(( $C + 1 ))
done

for name in ${real[*]};
do
	tmp=$(randomize)
	echo -e "$(date +"%s")\n$name -> $tmp\n" >> history.txt
	sudo cp $name $TARGET/$tmp.tar
done
sleep 10
done
