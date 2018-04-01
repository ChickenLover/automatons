import time
import sys
import itertools
from subprocess import call

terminal_length = 30
buffer_length = 28


one = '@'
zero = '_'


for rule in itertools.cycle([45, 60, 62, 72, 73, 74, 75, 82, 86, 88, 89, 90, 94, 101, 102, 104, 105, 106, 108, 109, 118, 120, 126, 134, 138, 144, 146, 148, 150, 166, 180, 182, 210]):
    ruleset = bin(rule)[2:].zfill(8)
    last_numbers = [0]*terminal_length
    try:
        while True:
            lines = []
            for _ in range(buffer_length):
                new_numbers = [1]
                for i in range(1, terminal_length-1):
                    prev_val = last_numbers[i-1]*4 + last_numbers[i]*2 + last_numbers[i+1]
                    new_numbers.append(bool(int(ruleset[prev_val])))
                new_numbers.append(1)
                last_numbers = new_numbers
                lines.append(last_numbers)
            time.sleep(0.1)
            to_print = ''
            for line in lines:
                to_print += '{}\n'.format(''.join([(one if number else zero) for number in line]))
            #call(['clear'])
            print('\n'*50)
            call(['cowsay', '-W', 40, to_print])
    except KeyboardInterrupt:
        pass
