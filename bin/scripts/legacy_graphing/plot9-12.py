import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#outfile = '/home/rxlx/bin/data/plots/graphs/rxlx-cpu.png'
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
ax.set_ylabel('load')
ax.set_title('rxlx CPU Util')
ten_mins = 0
sixty_mins = 0
count = 10
cpu_stats = np.loadtxt('uptime.plot')
cpu_avg10 = []
cpu_avg60 = []
marks_10 = []
marks_60 = []
while count <= len(cpu_stats):
    avg = 100 - (sum(cpu_stats[ten_mins:count]) / 10)
    cpu_avg10.append(avg)
    marks_10.append(ten_mins)
    ten_mins += 10
    count += 10

count = 60
while count <= len(cpu_stats):
    avg = 100 - (sum(cpu_stats[sixty_mins:count]) / 60)
    cpu_avg60.append(avg)
    marks_60.append(sixty_mins)
    sixty_mins += 60
    count += 60

x = [ 100 - e for e in cpu_stats ]

ax.plot()
ax.plot(x, color='#43AA8B', label='1m CPU avg')
#ax.scatter(marks_10, cpu_avg10, c='#666666')
ax.plot(marks_10, cpu_avg10, color='#FF101F', label='10m CPU avg')
#ax.scatter(marks_60, cpu_avg60, c='#ffffff')
ax.plot(marks_60, cpu_avg60, color='#ffffff', label='60m CPU avg')
legend = ax.legend(loc='upper center')
fig.savefig(storage'rxlx-cpu.png')
