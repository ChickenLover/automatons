import itertools
from subprocess import call
import time
import itertools
import os
import sys
from math import ceil
from termcolor import colored

from font import get_letters, get_train_letters, \
                 letter_w, letter_h, train_letter_w, train_letter_h

terminal_height, terminal_width = (int(x) - 1 for x in os.popen('stty size', 'r').read().split())
terminal_height -= 1
border = colored('|', 'red')
if len(sys.argv) > 2 and sys.argv[2] == 'train':
    letters = get_train_letters()
    letter_w = train_letter_w
    letter_h = train_letter_h
else:
    letters = get_letters()
text = ' ' + sys.argv[1].upper() + ' '
upper_bar = colored('/' + '-' * (terminal_width - 2) + '\\', 'red')
bottom_bar = colored('\\' + '-' * (terminal_width - 2) + '/', 'red')
empty_string = border + ' ' * (terminal_width - 2) + border
empty_height = (terminal_height - letter_h) // 2
max_shift = terminal_width - letter_w * len(text) - 2
colors_cycle = itertools.cycle(['red', 'blue', 'green', 'magenta',
                                'cyan', 'yellow'])
text_letters = [letters[x].split('\n') for x in text]

for shift in itertools.cycle(itertools.chain(range(max_shift), range(max_shift, 0, -1))):
    empty_right = ' ' * (terminal_width - letter_w * len(text) - shift - 2) + border
    empty_left = border + ' ' * shift
    letters_colors = [next(colors_cycle) for _ in range(len(text))]

    print(upper_bar)
    for i in range(empty_height):
        print(empty_string)
    for i in range(letter_h):
        text_str = ''.join([colored(x[i], letters_colors[j]) for j, x in enumerate(text_letters)])
        print(empty_left + text_str + empty_right)
    for i in range(empty_height):
        print(empty_string)
    print(bottom_bar)
    time.sleep(0.1)
    call(['printf', '"\033c"'])
