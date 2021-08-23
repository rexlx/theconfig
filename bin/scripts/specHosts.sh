#!/bin/bash

yes | cp -rf /etc/hosts /etc/hosts.Bak
wget http://someonewhocares.org/hosts/hosts
sed -i '/AWWJEEZ/q' /etc/hosts
cat ./hosts >> /etc/hosts
rm -rf ./hosts
