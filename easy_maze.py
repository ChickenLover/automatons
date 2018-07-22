from random import choice

l = 20
w = 30

for _ in range(l): print(''.join([choice(['/', '\\']) for _ in range(w)]))
