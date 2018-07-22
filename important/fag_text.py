import itertools
from subprocess import call
import time
import itertools
import os

from math import ceil
from termcolor import colored

from font import get_letters, letter_w, letter_h

texts = [x for x in \
'''
Crab
rave
'''.upper().split('\n') if x]
LENGTH = 1

terminal_height, terminal_width = (int(x) - 1 for x in os.popen('stty size', 'r').read().split())
terminal_height -= 2
border = colored('|', 'red')
upper_bar = colored('/' + '-' * (terminal_width - 2) + '\\', 'red')
bottom_bar = colored('\\' + '-' * (terminal_width - 2) + '/', 'red')
empty_string = border + ' ' * (terminal_width - 2) + border
empty_height = (terminal_height - letter_h) // 2
letters = get_letters()
colors_cycle = itertools.cycle(['red', 'blue', 'green', 'magenta',
                                'cyan', 'yellow'])
texts_letters = [[letters[x].split('\n') for x in text] for text in texts]
margins = [terminal_width - letter_w * len(text) - 2 for text in texts]
empty_rights = [' ' * (margins[i] // 2) + border for i in range(len(texts))]
empty_lefts = [border + ' ' * (margins[i] // 2) for i in range(len(texts))]

for step in itertools.cycle(range(len(texts))):
    for _ in range(LENGTH):
        next(colors_cycle)
        local_iter = iter(colors_cycle)
        letters_colors = [next(local_iter) for _ in range(len(texts[step]))]

        print(upper_bar)
        for i in range(empty_height):
            print(empty_string)
        for i in range(letter_h):
            text_str = ''.join([colored(x[i], letters_colors[j])\
                                for j, x in enumerate(texts_letters[step])])
            print(empty_lefts[step] + text_str + empty_rights[step])
        for i in range(empty_height):
            print(empty_string)
        print(bottom_bar)
        time.sleep(0.3)
        call(['printf', '"\033c"'])
