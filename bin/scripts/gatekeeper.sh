#!/bin/bash

nitro () {
  firewall-cmd --add-port=40818/tcp
  firewall-cmd --add-port=40818/udp
  firewall-cmd --add-port=40816/udp
  firewall-cmd --add-port=40816/tcp
}

rygal () {
  firewall-cmd --add-port=40812/tcp
  firewall-cmd --add-port=40812/udp
  
}

ssh () {
  firewall-cmd --add-port=40810/tcp
}
$@
