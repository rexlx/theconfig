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
ax.set_ylabel('bytes')
ax.set_title('Disk Util')

read = []
write = []

bytes_data = np.loadtxt('disk_bytes.plot', delimiter = ',')
b_read = [ x for x in bytes_data[:,0] ]
b_write = [ x for x in bytes_data[:,1] ]
five_mins =  b_read[-300:]
thirty_mins = b_read[-1800:]
r_one_hour = b_read[-3600:]
w_one_hour = b_write[-3600:]
#ax.plot(thirty_mins, color='#617066', label='bytes read')
ax.plot(r_one_hour, color='#DAE8EF', label='bytes read')
ax.plot(w_one_hour, color='#617066', label='bytes written')
#ax.plot(b_read, color='#617066', label='bytes read')
#ax.plot(b_write, color='#DAE8EF', label='bytes written')
legend = ax.legend(loc='upper center')
fig.savefig('rxlx-bytes.png', dpi = 300)
