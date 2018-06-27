import time
import math

one_char = '+'
zero_char = ' '
step = 0.08
size = 120
half = size//2

def sin_arr(i):
   return ''.join([one_char if j == int(i*half) else zero_char for j in range(-half, half)])

i = 0

while True:
    print(sin_arr(math.sin(i)))
    i += step
    time.sleep(0.05)
