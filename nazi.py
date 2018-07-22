import time
from itertools import cycle, chain


def main():
    msg0 = 'Roma <3 卍'
    msg1 = '卍 <3 Romu'

    msg = msg0
    iterator = cycle(chain(range(120), reversed(range(120))))
    while True:
        try:
            print(' '*next(iterator) + msg)
            time.sleep(0.05)
        except KeyboardInterrupt:
            print(' ')
            if msg == msg0:
                msg = msg1
            else:
                msg = msg0


if __name__=="__main__":
    main()

