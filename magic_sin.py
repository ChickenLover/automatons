import time
import math

step = 0.06
size = 60
half = size//2
zero_char = ' '
cross_char = '+'

def get_char(x, next_x):
    x_pos = int(x*half) + 50
    next_x_pos = int(next_x*half) + 50
    if x_pos == next_x_pos:
        return '||'
    if x_pos < next_x_pos:
        return '\\\\'
    if x_pos > next_x_pos:
        return '//'

def get_arr(x, next_x):
    return ''.join([get_char(x, next_x) if j == int(x*half) else zero_char for j in range(-half, half)])

def sin_arr(x):
    sin = math.sin(x)
    next_sin = math.sin(x+step)
    return get_arr(sin, next_sin)

def cos_arr(i, step):
    i = math.cos(i)
    next_i = math.cos(i+step)
    return get_arr(i, next_i)

def tg_arr(i, step):
    i = math.tan(i)
    next_i = math.tan(i+step)
    return get_arr(i, next_i)

def merge(ars):
    ret = ''
    for i in range(size):
        char = None
        for ar in ars:
            if not ar[i] == zero_char:
                if char:
                    char = cross_char
                    break
                char = ar[i]
        ret += char if char else zero_char
    return ret

i = 0

while True:
    print(sin_arr(i))
    i += step
    time.sleep(0.02)
