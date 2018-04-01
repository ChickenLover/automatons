import time
import sys
import itertools


terminal_length = 120

one = '@'
zero = '_'


for rule in itertools.cycle([45, 60, 62, 72, 73, 74, 75, 82, 86, 88, 89, 90, 94, 101, 102, 104, 105, 106, 108, 109, 118, 120, 126, 134, 138, 144, 146, 148, 150, 166, 180, 182, 210]):
    ruleset = bin(rule)[2:].zfill(8)
    last_numbers = [0]*terminal_length
    last_numbers[int(len(last_numbers)/2)] = 1
    try:
        while True:
            new_numbers = [0]
            for i in range(1, terminal_length-1):
                prev_val = last_numbers[i-1]*4 + last_numbers[i]*2 + last_numbers[i+1]
                new_numbers.append(bool(int(ruleset[prev_val])))
            new_numbers.append(0)
            print(''.join([(one if number else zero) for number in new_numbers]), rule)
            last_numbers = new_numbers
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
