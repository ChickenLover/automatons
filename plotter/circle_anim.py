import time
from itertools import cycle, chain

from plotter import *
from sin_anim import plot_sin


X_length = 125
Y_length = 125

field = BrailleField(X_length, Y_length)

for i in cycle(range(X_length, 0, -1)):
    field.clear()
    for shift in range(0, Y_length, 10):
        field.plot_circle(Point(X_length//2, Y_length//2), (i + shift) % Y_length)
    #update_field(field)
    print(field)
    time.sleep(0.01)
