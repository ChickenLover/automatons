import numpy as np
from itertools import cycle
import time

from plotter import *

X_length = 125
Y_length = 125

field = BrailleField(X_length, Y_length)

radius = Y_length//2
n = 100
mul_from = 2
mul_to =100
mul_step = 0.01
length = 2 * np.pi / n


def draw_time_table(m):
    field.clear()
    field.plot_circle(Point(X_length//2, Y_length//2), radius)
    for i in range(n):
        first = Point(np.cos(i*length) * radius + radius, np.sin(i*length) * radius + radius)
        second = Point(np.cos(i*m*length) * radius + radius, np.sin(i*m*length) * radius + radius)
        if first != second:
            field.plot_line(first, second)

for m in np.linspace(mul_from, mul_to, 1/mul_step*(mul_to - mul_from)):
    draw_time_table(m)
    #field.plot_line(Point(100, 100), Point(0, 0))
    update_field(field)
    time.sleep(0.025)
