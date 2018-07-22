from itertools import cycle, chain
import time
from math import sqrt, cos, sin, pi


from plotter import *

X_length = 125
Y_length = 125

field = BrailleField(X_length, Y_length)
radius = Y_length//3
circle_radius = Y_length//2
step = -0.1
O = Point(X_length // 2, Y_length // 2)


def draw_edge(a):
    for i in range(4):
        edge_b = a + (i * pi/2)
        edge_a = edge_b + pi/4
        A = Point(cos(edge_a) * radius + O.x, sin(edge_a) * radius + O.y)
        B = Point(cos(edge_b) * sqrt(2) * radius + O.x, sin(edge_b) * sqrt(2) * radius + O.y)
        field.plot_line(O, A);
        field.plot_line(A, B);

for i in cycle(range(500)):
    field.clear()
    draw_edge(i * step)
    field.plot_circle(O, circle_radius)
    update_field(field)
    time.sleep(0.05)
