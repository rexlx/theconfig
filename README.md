# theconfig
shell script containing semi-useful commands as well as a collection of python scripts. In addition, a collection of aliases located in the data directory can extend the functionality of this tool.

$HOME/bin/ is where i keep all of my binaries, its usually on the path by default
<br>
needs to be executable and on your path. for easy install run (as non root user):

```bash
mkdir ~/bin/
mkdir ~/tmp/
cd ~/tmp/
git clone https://github.com/rexlx/theconfig.git
mv theconfig/bin/* ~/bin/
chmod +x ~/bin/theconfig
vi ~/.bashrc
# at the very bottom of the file add the following line
source ~/bin/theconfig
# press esc then type :wq <enter> to write and quit
rm -rf ~/tmp/
. ~/.bashrc
(to confirm install run)
viconfig
# press esc then type :wq <enter> to write and quit
```
<br><hr>
list of commands it gives you:

```
viconfig        edit config file
up              get uptime
border          create border around a string
center          center a string and fill in whitespace
dstamp          date stamp 11/02/2017 08:07:04 AM
fstamp          format for files 2022-04-05_07-14
ustamp          unique stamp 1509628041
grip            grep for IP's
grip-2          grip + only show IP
dns             get the IP of the dns youre using
showport        show firewalld status
model           get machine model
virt            see if machine is bare metal or not
normalize       install some common packages
clear-ram       clear ram and cache (must be root)
sysinf          get the system info of the local machine
get-sysinf      get the system ifo of a remote machine
mark-user       turns the prompt red to warrant caution
top-mem         ten most memory intensive procs
show-writes     show amount of reads / writes since booted.
keep-alive      keep current terminal alive
convert-size    converts bytes to human readable
watch-access    tail httpd access logs
foreach         simple foreach boiler plate ($ foreach ls)
isword          spell checker when on headless system
top-ten         show ten most expensive cpu processes
convert-time    unix time -> date time
convert-date    date time -> unix time
add-comma       add commas to large numbers
describe        pandas describe a csv ($ describe file.csv)
```
