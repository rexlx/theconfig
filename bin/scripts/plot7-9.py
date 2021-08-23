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
ax.set_title('lan from rxlx')

rxap_stats = np.loadtxt('rxap.plot')
surx_stats = np.loadtxt('surx.plot')
gw_stats = np.loadtxt('GW.plot')
ax.plot(rxap_stats, color='#B3EFB2', label='rxap')
ax.plot(surx_stats, color='#E15554', label='surx')
ax.plot(gw_stats, color='#4E5283', label='GW')
legend = ax.legend(loc='upper center')

fig.savefig('rxlx7-9.png')
