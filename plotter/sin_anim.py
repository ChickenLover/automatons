import time
from itertools import cycle, chain

from math import sin, pi, cos

from plotter import *


def plot_sin(field, shift):
    sin_func = lambda t: 3 + (Y_length//2-3)*(sin(((t+shift)/(X_length//2)-1)*pi)+1)
    field.plot_function(func_y=sin_func)
    field.plot_circle(Point(X_length//2-1, sin_func(X_length//2-1)), 3)

if __name__ == '__main__':
    X_length = 250
    Y_length = 125//2

    field = BrailleField(X_length, Y_length)
    for i in cycle(range(X_length)):
        field.clear()
        plot_sin(field, i)
        #update_field(field)
        print(field)
        time.sleep(0.01)
