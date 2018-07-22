import itertools
from string import ascii_uppercase, digits

letter_w = 25
letter_h = 21

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def get_letters():
    letters = {x: list() for x in range(26)}

    raw = open('fonts/raw.txt').read()
    for row in raw.split('\n'):
        for i, chunk in enumerate(grouper(row, 33)):
            chunk = ''.join([x for x in chunk if x])
            letters[i].append(chunk[:letter_w])

    raw2 = open('fonts/raw2.txt').read()
    for row in raw2.split('\n'):
        for i, chunk in enumerate(grouper(row, 33)):
            chunk = ''.join([x for x in chunk if x])
            letters[i + 12].append(chunk[:letter_w])

    raw3 = open('fonts/raw3.txt').read()
    for row in raw3.split('\n'):
        for i, chunk in enumerate(grouper(row, 33)):
            chunk = ''.join([x for x in chunk if x])
            letters[i + 20].append(chunk[:letter_w])

    raw4 = open('fonts/raw4.txt').read()
    for row in raw4.split('\n'):
        for i, chunk in enumerate(grouper(row, 33)):
            chunk = ''.join([x for x in chunk if x])
            letters[i + 22].append(chunk[:letter_w])


    letters = {ascii_uppercase[x]: '\n'.join(letters[x]) for x in range(26)}
    letters[' '] = '\n'.join([' ' * letter_w for _ in range(letter_h)])
    return letters

train_letter_w = 8
train_letter_h = 6
def get_train_letters():
    symbols = {x: list() for x in range(38)}

    raw = open('fonts/train.txt').read()
    for row in raw.split('\n'):
        for i, chunk in enumerate(grouper(row, train_letter_w)):
            chunk = ''.join([x for x in chunk if x])
            symbols[i].append(chunk[:train_letter_w])
    letters = {ascii_uppercase[x]: '\n'.join(symbols[x]) for x in range(26)}
    letters.update({digits[x - 26]: '\n'.join(symbols[x]) for x in range(25, 35)})
    letters['!'] = '\n'.join(symbols[36])
    letters[' '] = '\n'.join([' ' * train_letter_w for _ in range(train_letter_h)])
    return letters
