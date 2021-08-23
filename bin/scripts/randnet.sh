#!/bin/bash


IFACE=$(ip route get 8.8.8.8 | awk '{ print $5 }')
ID=$(id -u)


if [[ $ID != 0 ]]; then
  clear
  echo -e "\n\nThis script may require elevated permissions!!\n"
else
  clear
fi

grip () {
  grep -E -o '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
}


center() {
  termwidth="$(tput cols)"
  padding="$(printf '%0.1s' ={1..500})"
  printf '%*.*s %s %*.*s\n' 0 "$(((termwidth-2-${#1})/2))" "$padding" "$1" 0 "$(((termwidth-1-${#1})/2))" "$padding"
}

stop () {
  tc qdisc del dev $IFACE root
  return
}

start () {
  tc qdisc add dev $IFACE root handle 1: prio
  tc qdisc add dev $IFACE parent 1:3 handle 30: netem delay 10ms loss 10%
  tc filter add dev $IFACE protocol ip parent 1:0 prio 3 u32 match ip dst 10.16.180.0/24 flowid 1:3
  return
}

dtime () {
  shuf -n 1 -e {1..25}ms
  return
}

ltime () {
  shuf -n 1 -e {1..12}%
  return
}

stop
start

while [ true ]; do
  tc qdisc change dev $IFACE parent 1:3 handle 30: netem delay $(dtime) loss $(ltime)
  sleep 1200
done
