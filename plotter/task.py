from collections import namedtuple
import socket
import re
from plotter import *
import time

def get_params(n, topleft, bottomright, t, o_quad):
    width = bottomright.x - topleft.x + 1
    heigth = bottomright.y - topleft.y + 1
    if t == 0:
        quad = 1
        n_topleft = Point(topleft.x, topleft.y)
        n_bottomright = Point(bottomright.x - (width // 2), bottomright.y - (heigth // 2))
    elif t == 1:
        quad = 2 
        n_topleft = Point(topleft.x + (width//2), topleft.y)
        n_bottomright = Point(bottomright.x, bottomright.y - (heigth // 2))
    elif t == 2:
        quad = 3
        n_bottomright = Point(bottomright.x, bottomright.y)
        n_topleft = Point(topleft.x + (width//2), topleft.y + (heigth//2))
    elif t == 3:
        quad = 0
        n_topleft = Point(topleft.x, topleft.y + (heigth//2))
        n_bottomright = Point(bottomright.x - (width//2), bottomright.y)
    elif t == 4:
        quad = o_quad
        qw = width//4
        qh = heigth//4
        n_topleft = Point(topleft.x + qw, topleft.y + qh)
        n_bottomright = Point(bottomright.x - qw, bottomright.y - qh)
    #print(f'Params for type={t}, topleft={topleft}, bottomright={bottomright}:\nn_topleft={n_topleft}, n_bottomright={n_bottomright}')
    return (n - 1, n_topleft, n_bottomright, quad)


class L:
    nodes = []

    def __init__(self, *nodes):
        self.nodes = nodes

    def __repr__(self):
        return 'L[{}, {}, {}]'.format(*self.nodes)


def build_l(n, topleft, bottomright, quad):
    if n == 2:
        #topright
        if quad == 0:
            return [L(topleft, Point(topleft.x, bottomright.y), bottomright)]
        #bottomrigth
        elif quad == 1:
            return [L(topleft, Point(topleft.x, bottomright.y), Point(bottomright.x, topleft.y))]
        #bottomleft
        elif quad == 2:
            return [L(topleft, Point(bottomright.x, topleft.y), bottomright)]
        #topleft
        elif quad == 3:
            return [L(Point(bottomright.x, topleft.y), Point(topleft.x, bottomright.y), bottomright)]
    width = bottomright.x - topleft.x + 1
    heigth = bottomright.y - topleft.y + 1
    #topright
    if quad == 0:
        return [x for i in [0, 2, 3, 4] for x in build_l(*get_params(n, topleft, bottomright, i, quad))]
    #bottomrigth
    elif quad == 1:
        return [x for i in [0, 1, 3, 4] for x in build_l(*get_params(n, topleft, bottomright, i, quad))]
    #bottomleft
    elif quad == 2:
        return [x for i in [0, 1, 2, 4] for x in build_l(*get_params(n, topleft, bottomright, i, quad))]
    #topleft
    elif quad == 3:
        return [x for i in [1, 2, 3, 4] for x in build_l(*get_params(n, topleft, bottomright, i, quad))]


def get_square_quad(square, topleft, bottomright):
    square -= topleft
    bottomright -= topleft
    topleft = Point(0, 0)
    width = bottomright.x - topleft.x + 1
    heigth = bottomright.y - topleft.y + 1
    if square.y < (heigth // 2) and square.x >= (width // 2): return 0
    if square.y >= (heigth // 2) and square.x >= (width // 2): return 1
    if square.y >= (heigth // 2) and square.x < (width // 2): return 2
    if square.y < (heigth // 2) and square.x < (width // 2): return 3


"""import time
while True:
    time.sleep(1)
    sock = socket.socket()
    sock.connect(('misc.chal.csaw.io', 9000))
    res = sock.recv(1024)
    try:
        marked = re.search('\((\d+\d+, \d+\d+)\)', sock.recv(1024).decode()).group(1)
    except:
        continue
    marked = Point(*[int(x) for x in marked.split(', ')])
    print(marked)"""


els = list()
n = 6
topleft = Point(0, 0)
bottomright = Point(63, 63)
marked = Point(12, 8)

field = Field(64, 64)
field.plot_dots(marked)

while n:
    quad = get_square_quad(marked, topleft, bottomright)
    ls = build_l(n+1, topleft, bottomright, quad)
    for l in ls:
        field.plot_dots(*l.nodes, dot=str(7 - n))
        update_field(field)
    els.extend(ls)
    width = bottomright.x - topleft.x + 1
    heigth = bottomright.y - topleft.y + 1
    if quad == 0:
        topleft.x += width//2
        bottomright.y -= heigth//2
    elif quad == 1:
        topleft.x += width//2
        topleft.y += heigth//2
    elif quad == 2:
        bottomright.x -= width//2
        topleft.y += heigth//2
    elif quad == 3:
        bottomright.x -= width//2
        bottomright.y -= heigth//2
    n -= 1
