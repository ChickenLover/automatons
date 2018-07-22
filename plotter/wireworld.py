import time
from itertools import cycle, chain

from math import sin, pi

from plotter import *


X_length = 120
Y_length = 32


cells = [' ', '-', 'x', 'o']
cells_enum = {y: x for x, y in enumerate(cells)}


field = Field(X_length, Y_length, ' ', 'o')


def update_point(point):
    cell = cells_enum.get(field.get_dot(point), None)
    if not cell: return 0
    if cell == 1: return 4
    if cell == 2: return 1
    if cell == 4:
        alive = sum([int(cells_enum.get(field.get_dot(n_point), 0) == 2)\
                     for n_point in field.get_neighbours(point)])
        if alive and alive < 3: return 2
        return 4


def update_cells():
    for y in Y_length:
        for x in X_length:
            p = Point(x, y)
            field.plot_dot(p, cells[update_point(p)])

while True:
    update_cells()
    update_field()
    time.sleep(1)

for i in cycle(range(X_length)):
    field.fill()
    plot_sin(i)
    update_field(field)
    time.sleep(0.05)
