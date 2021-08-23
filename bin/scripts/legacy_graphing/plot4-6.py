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
ax.set_title('Music Services from rxlx')

pnd_stats = np.loadtxt('pandora.plot')
pms_stats = np.loadtxt('playMusic.plot')
five_mins = 0
count = 10
pan_avg5 = []
ply_avg5 = []
pan_x = []
ply_x = []
while count <= len(pnd_stats):
    avg = sum(pnd_stats[five_mins:count]) / 10
    pan_avg5.append(avg)
    pan_x.append(five_mins)
    five_mins += 10
    count += 10
five_mins = 0
count = 10
while count <= len(pms_stats):
    avg = sum(pms_stats[five_mins:count]) / 10
    ply_avg5.append(avg)
    ply_x.append(five_mins)
    five_mins += 10
    count += 10

#rxmini_stats = np.loadtxt('rxmini.plot')
#cpuX = list(range(1, len(cpu_stats)))
ax.plot(pnd_stats, color='#1440ce', label='pandora')
ax.plot(pms_stats, color='#e27616', label='play music')
ax.plot(pan_x, pan_avg5, color='#94C9A9', label='average-1')
ax.plot(ply_x, ply_avg5, color='#777DA7', label='average-2')
#ax.plot(rxmini_stats, color='#AA9FB1', label='rxmini')
legend = ax.legend(loc='upper center')
fig.savefig('rxlx4-6.png')
