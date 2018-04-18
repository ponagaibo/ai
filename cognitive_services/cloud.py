from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

x = [0,1,2,3]
freq = [100,200,300,400]
width = 0.8 # width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, freq, width, color='r')

ax.set_ylim(0,450)
ax.set_ylabel('Frequency')
ax.set_title('Insert Title Here')
ax.set_xticks(np.add(x,(width/2))) # set the position of the x ticks
ax.set_xticklabels(('X1', 'X2', 'X3', 'X4', 'X5'))

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)

plt.show()