import time

import numpy as np

from plotter import *


X_length = 120
Y_length = 60
DENSITY = 6


field = BrailleField(X_length, Y_length)
field.random_fill(low=DENSITY, high=DENSITY)
print(field)

while True:
    next_gen = np.zeros((X_length, Y_length), dtype='bool')
    for point in field.points_iter():
        neis = field.get_neighbours(point)
        alive = sum(field.if_dot(p) for p in neis)
        coords = tuple(point)
        if alive == 3:
            next_gen[coords] = 1
        elif alive == 2:
            next_gen[coords] = field.if_dot(point)
        else:
            next_gen[coords] = 0
    field.clear()
    for (x, y), _ in np.ndenumerate(np.where(next_gen)):
        field.plot_dots(Point(x, y))
    time.sleep(0.1)
    update_field(field)
