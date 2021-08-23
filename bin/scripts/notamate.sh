send "bin/rcpu -r 60 -R 4" -f ~/bin/data/nodes.txt -u rxlx -t 300
for i in $(cat ~/bin/data/nodes.txt); do scp rxlx@$i:~/cpuutil.csv /Volumes/surx/stats/$i-cpuutil.csv; done
