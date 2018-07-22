import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.animation as anim
import numpy as np
import matplotlib
from itertools import cycle

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1,1,1)
ax.set_xlim((-1,1))
ax.set_ylim((-1,1))

c_lin = np.linspace(0,1,200)
color=cycle(cm.rainbow(c_lin.tolist() + c_lin.tolist()[::-1]))

def draw_time_table(m):
    c=next(color)
    n = 200
    ax.clear()
    circle = plt.Circle((0, 0), 1, fill=False)
    ax.add_artist(circle)
    length = 2 * np.pi / n
    for i in range(n):
        first = (np.cos(i*length), np.sin(i*length))
        second = (np.cos(i*m*length), np.sin(i*m*length))
        if first != second:
            ax.plot([first[0], second[0]], [first[1], second[1]], c=c)
            
mul_from = 2
mul_to =100
mul_step = 0.01

Writer = anim.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=3600)

a = anim.FuncAnimation(fig, draw_time_table, frames=np.arange(mul_from, mul_to, mul_step), interval=10)
a.save('timetables_set.mp4', writer=writer)

