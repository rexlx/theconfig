import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

storage = '/home/rxlx/bin/data/plots/graphs'
fig = plt.figure()
ax = fig.add_subplot(111, facecolor='k')
ax.grid(color='#565857', linestyle='-', linewidth=0.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)
ax.spines['bottom'].set_color('green')
ax.spines['left'].set_color('blue')
ax.title.set_color('k')
ax.yaxis.label.set_color('k')
ax.xaxis.label.set_color('k')
ax.tick_params(axis='x', colors='blue')
ax.tick_params(axis='y', colors='blue')

ax.tick_params(axis='both', direction='in')
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax.set_xlabel('time')
ax.set_ylabel('ms')
ax.set_title('internet diag from rxlx')
aws_stats = np.loadtxt('amazon.plot')
dns_stats = np.loadtxt('DNS.plot')
#wkp_stats = np.loadtxt('wikipedia.plot')
#dnsX = list(range(1, len(dns_stats)))
#wkpX = list(range(1, len(wkp_stats)))

aws_stats = np.loadtxt('amazon.plot')
dns_stats = np.loadtxt('DNS.plot')
five_mins = 0
count = 10
aws_avg5 = []
dns_avg5 = []
aws_x = []
dns_x = []
while count <= len(aws_stats):
    avg = sum(aws_stats[five_mins:count]) / 10
    aws_avg5.append(avg)
    aws_x.append(five_mins)
    five_mins += 10
    count += 10
five_mins = 0
count = 10
while count <= len(dns_stats):
    avg = sum(dns_stats[five_mins:count]) / 10
    dns_avg5.append(avg)
    dns_x.append(five_mins)
    five_mins += 10
    count += 10

ax.plot(aws_x, aws_avg5, color='#ed9404', label='average-1')
ax.plot(dns_x, dns_avg5, color='#e21e04', label='average-2')
ax.plot(aws_stats, color='#D7FCD4', label='amazon')
ax.plot(dns_stats, color='#0080ff', label='dns_gl')
legend = ax.legend(loc='upper center')
fig.savefig('rxlx1-3.png')
