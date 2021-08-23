# theconfig
simple shell script containing semi-useful commands for redhat/redhat-like systems(doesnt seem to work in zsh environment)

Needs to be executable and on your path. for easy install run (as non root user):

```bash
mkdir ~/bin/
mkdir ~/tmp/
cd ~/tmp/
git clone https://github.com/rexlx/theconfig.git
mv theconfig/bin/* ~/bin/
chmod +x ~/bin/theconfig
vi ~/.bashrc
(at the very bottom of the file add the following line)
source ~/bin/theconfig
rm -rf ~/tmp/
. ~/.bashrc
(to confirm install run)
viconfig
```
<br><hr>
list of commands it gives you:

```
up
ipv4
fwl
gw
iface
slnx
border
center
dstamp
fstamp
ustamp
grip
grip-2
dns
defnet
showport
model
virt
rl
clients
tshootnet
logStamp
fastlog
log
normalize
clear-ram
sysinf
get-sysinf
viconfig
mark-user
top-mem
kill-tracker
show-writes
keep-alive
convert-size
fix-db
watch-access
getip
foreach
isword
top-ten
convert-time
convert-date
add-comma
describe
```
