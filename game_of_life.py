import random
import time
from subprocess import call 

field_size_x = 70
field_size_y = 30

spawn_rate = 15

zero = ' '
one = '@'
two = '卍'
cur = one

last_field = []
for _ in range(field_size_y):
    last_field.append([random.randint(0,spawn_rate)//(spawn_rate-1) for __ in range(field_size_x)])

def print_field(f):
    call(['clear'])
    for l in f:
        print(''.join(cur if el else zero for el in l))

while True:
    try:
        print_field(last_field)
        new_field = []
        new_field.append([0]*field_size_x)
        for y in range(1, field_size_y-1):
            line = []
            line.append(0)
            for x in range(1, field_size_x-1):
                alive_neighbors = 0
                alive_neighbors += last_field[y-1][x-1] + last_field[y-1][x] + last_field[y-1][x+1] + last_field[y][x-1] + last_field[y][x+1] + last_field[y+1][x-1] + last_field[y+1][x] + last_field[y+1][x+1]
                if alive_neighbors == 3:
                    line.append(1)
                    continue
                if alive_neighbors > 3 or alive_neighbors < 2:
                    line.append(0)
                else:
                    line.append(last_field[y][x])
            line.append(0)
            new_field.append(line)
        new_field.append([0]*field_size_x)
        last_field = new_field
        time.sleep(0.1)
    except KeyboardInterrupt:
        if cur == one:
            cur = two
        else:
            cur = one
