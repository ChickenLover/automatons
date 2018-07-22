import time
from itertools import cycle, chain

from math import sin, pi, cos

from plotter import *

text = '_Vinya_'
text2 = '_Pidor_'

if __name__ == '__main__':
    X_length = 120
    Y_length = 16

    field = Field(X_length, Y_length)
    sin_func = lambda t: 3 + (Y_length//2-3)*(sin(((t)/(X_length//2)-1)*pi)+1)
    for x, symbol, symbol2 in zip(range(X_length), cycle(text), cycle(text2)):
        field.plot_dots(Point(x, int(sin_func(x))), dot=symbol)
        field.plot_dots(Point(x, int(Y_length - sin_func(x))), dot=symbol2)
    print(field)

