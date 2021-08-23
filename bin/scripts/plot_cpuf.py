import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.add_subplot(111, facecolor='k')
ax.grid(color='#565857', linestyle='-', linewidth=0.5)
#ax.spines['top'].set_visible(True)
#ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_linewidth(1)
#ax.spines['bottom'].set_color('green')
#ax.spines['left'].set_color('blue')
ax.title.set_color('k')
ax.yaxis.label.set_color('k')
ax.xaxis.label.set_color('k')
ax.tick_params(axis='x', colors='blue')
ax.tick_params(axis='y', colors='blue')
ax.tick_params(axis='both', direction='in')
#ax.get_xaxis().tick_bottom()
#ax.get_yaxis().tick_left()
ax.set_xlabel('time')
ax.set_ylabel('frequency')
ax.set_title('cpu stats')


data = np.loadtxt('cpuutil.plot', delimiter = ',')
cpu = [ x for x in data[:,0] ]
cpu_freq = [ x for x in data[:,1] ]

#r_one_hour = r_ops[-3600:]
#w_one_hour = w_ops[-3600:]

ax.plot(cpu_freq, color='#FF5733', label='cpu freq')
#ax.plot(w_one_hour, color='#43AA8B', label='write ops')

#ax.plot(r_ops, color='#43AA8B', label='read ops')
#ax.plot(w_ops, color='#FF5733', label='write ops')
legend = ax.legend(loc='upper center')
fig.savefig('cpu_freq.png', dpi = 250)
