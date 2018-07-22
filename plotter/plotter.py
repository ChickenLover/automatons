from random import randint, shuffle
from subprocess import call
from math import hypot, cos, sin, pi, ceil

BRAILLE_START_CODE = 10240


def random_point(x_from, x_to, y_from, y_to):
    return Point(randint(x_from, x_to), randint(y_from, y_to))


class Point():
    def __init__(self, x=0, y=0):
        if x < 0 or y < 0:
            pass
            #raise NegativeCoordinatesException(
            #        'Can\'t create point with the negative coordinates')
        self.x = x
        self.y = y

    def __iter__(self):
        return iter([self.x, self.y])

    def __len__(self):
        return 2

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return 'Point({x}, {y})'.format(x=self.x, y=self.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __abs__(self):
        return hypot(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + -other

    def to_braille_power(self):
        return BRAILLE_SYMBOL_POWERS[self.x % 4 % 2][self.y % 4] + 8 * int(self.x % 4 > 1)


BRAILLE_SYMBOL_POWERS = {0: {0: 6,
                             1: 2,
                             2: 1,
                             3: 0},
                         1: {0: 7,
                             1: 5,
                             2: 4,
                             3: 3}}


class BrailleBlock():

    dots = 0

    def __init__(self, fill='None'):
        if fill == 'all': self.fill()
        elif fill == 'random': self.randomize()

    def if_dot(self, p):
        return (self.dots >> p.to_braille_power()) % 2

    def plot_dot(self, p):
        self.dots |= 2 ** p.to_braille_power()

    def fill(self):
        self.dots = 2 ** 16 - 1

    def random_fill(self, low=0, high=16):
        ones = randint(low, high)
        bins = list(str(bin(sum(2 ** i for i in range(ones))))[2:].zfill(16))
        shuffle(bins)
        self.dots = int(''.join(bins), 2)

    def clear(self):
        self.dots = 0

    def __str__(self):
        return chr(BRAILLE_START_CODE + self.dots % 256) +\
               chr(BRAILLE_START_CODE + (self.dots >> 8))
 
    def __repr__(self):
        return 'BrailleBlock({})'.format(self)


class Line():
    def __init__(self, p1, p2):
        if p1 == p2:
            raise InfiniteException('There infinitely many lines with such points')
        if p1.x == p2.x:
            self.p1 = p1 if p1.y <= p2.y else p2
            self.p2 = p2 if p1.y <= p2.y else p1
        else:
            self.p1 = p1 if p1.x <= p2.x else p2 
            self.p2 = p2 if p1.x <= p2.x else p1


class PlotterException(Exception):
    pass


class OutOfBoundsException(PlotterException):
    pass


class NegativeCoordinatesException(PlotterException):
    pass


class InfiniteException(PlotterException):
    pass




class BrailleField:

    field = None

    def __init__(self, x_length=25, y_length=10):
        self.width = ceil(x_length / 4) * 4
        self.height = ceil(y_length / 4) * 4
        self.init_blocks()
    
    def init_blocks(self):
        self.field = [[BrailleBlock() for _ in range(self.width // 4)]\
                      for _ in range(self.height // 4)]

    def __iter__(self):
        for i in range(self.width // 4):
            for j in range(self.height // 4):
                yield self.field[j][i]
    
    def points_iter(self):
        for i in range(self.width):
            for j in range(self.height):
                yield Point(i, j)

    def clear(self):
        for block in self: block.clear()

    def fill(self):
        for block in self: block.fill()

    def random_fill(self, low=0, high=16):
        for block in self: block.random_fill(low, high)

    def plot_dots(self, *points):
        for point in points:
            if not self.point_in_range(point):
                continue
                #raise OutOfBoundsException('The point is out of plotter range')
            self[point].plot_dot(point)

    def plot_line(self, p1, p2):
        if p1.x > p2.x: p1, p2 = p2, p1
        m = (p2.y - p1.y) / (p2.x - p1.x)
        b = p1.y - m * p1.x
        self.plot_function(rng=(int(p1.x), ceil(p2.x)),  func_y=lambda x: m*x + b)

    def if_dot(self, point):
        return self[point].if_dot(point)
    
    def point_in_range(self, point):
        return point.x < self.width and point.y < self.height and point.x >= 0 and point.y >= 0

    def plot_function(self, func_x=None, func_y=None, rng=None):
        if rng is None: rng = (0, self.width) if func_x is None else (0, self.height)
        if func_x is None: func_x = lambda t: t
        if func_y is None: func_y = lambda t: t
        for t in range(*rng):
            self.plot_dots(Point(int(func_x(t)), int(func_y(t))))

    def plot_circle(self, center, r):
        self.plot_function(func_x=lambda t: cos(t/200 * 2 * pi) * r + center.x,
                            func_y=lambda t: sin(t/200 * 2 * pi) * r + center.y,
                            rng=(0, 200))

    def get_neighbours(self, point):
        return filter(self.point_in_range,
                      [Point(point.x + j, point.y + i)\
                              for i in range(-1, 2)\
                              for j in range(-1, 2)])

    def __getitem__(self, key):
        if len(key) == 2:
            x, y = key
            return self.field[(self.height - 1 - y) // 4][x // 4]
        raise KeyError('')

    def __str__(self):
        string_repr = '/' + '-' * (self.width // 2) + '\\\n'
        for line in self.field: string_repr += '|{}|\n'.format(''.join(str(x) for x in line))
        string_repr += '\\' + '-' * (self.width // 2) + '/'
        return string_repr

    def __repr__(self):
        return str(self)


class Field():

    def __init__(self, x_length=25, y_length=10, whitespace=' ', dot='o'):
        self.width = x_length
        self.height = y_length
        self.whitespace = whitespace
        self.fill()
        self.dot = dot
    
    def fill(self, char=None):
        if char is None: char = self.whitespace
        self.field = [[char for _ in range(self.width)] for _ in range(self.height)]

    def invert(self):
        for i in range(self.width * self.height):
            p = Point(i // self.height, i % self.width)
            if self.if_dot(p): self.plot_dots(p, dot=self.whitespace)
            else: self.plot_dots(p)

    def point_in_range(self, point):
        return point.x < self.width and point.y < self.height and point.x >= 0 and point.y >= 0
    
    def if_dot(self, point):
        return self.field[self.height - 1 - point.y][point.x] != self.whitespace
    
    def get_dot(self, point):
        if not self.point_in_range(point): return None
        return self.field[self.height - 1 - point.y][point.x]
    
    def find_dots(self, dot):
        for i in range(self.height):
            for j in range(self.width):
                field_dot = self.field[self.height - 1 - i][j]
                if field_dot == dot: yield Point(j, i)

    def get_neighbours(self, point):
        return filter(self.point_in_range,
                      [Point(point.x + j, point.y + i)\
                              for i in range(-1, 2)\
                              for j in range(-1, 2)])

    def get_close_neighbours(self, point):
        return [p for p in self.get_neighbours(point) if abs(p - point) == 1]

    def plot_dots(self, *points, dot=None):
        if dot is None: dot = self.dot
        for point in points:
            if not self.point_in_range(point):
                continue
                #raise OutOfBoundsException('The point is out of plotter range')
            self.field[self.height - 1 - point.y][point.x] = dot

    def plot_function(self, func_x=None, func_y=None, rng=None, dot=None):
        if rng is None: rng = (0, self.width) if func_x is None else (0, self.height)
        if func_x is None: func_x = lambda t: t
        if func_y is None: func_y = lambda t: t
        for t in range(*rng):
            self.plot_dots(Point(int(func_x(t)), int(func_y(t))), dot=dot)

    def plot_line(self, line):
        for point in [line.p1, line.p2]:
            if not self.point_in_range(point):
                raise OutOfBoundsException('The line goes beyond range')
        p1 = line.p1
        p2 = line.p2
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if dx and dy:
            k = dy / dx
            b = (p1.y*dx - p1.x*dy) / dx
            print(k, b)
            self.plot_function(y_func=lambda t: t*k + b, rng=(p1.x, p2.x + 1))
        elif dy:
            self.plot_function(x_func=lambda t: p1.x, rng=(p1.y, p2.y + 1))
        else:
            self.plot_function(y_func=lambda t: p1.y, rng=(p1.x, p2.x + 1))

    def plot_circle(self, center, r, dot=None):
        self.plot_function(func_x=lambda t: cos(t/200 * 2 * pi) * r + center.x,
                            func_y=lambda t: sin(t/200 * 2 * pi) * r + center.y,
                            rng=(0, 200),
                            dot=dot)

    def __str__(self):
        string_repr = ''
        string_repr += '/' + '-' * self.width + '\\\n'
        for line in self.field: string_repr += '|{}|\n'.format(''.join(line))
        string_repr += '\\' + '-' * self.width + '/'
        return string_repr

    def __repr__(self):
        return str(self)


def update_field(field):
    call(['printf', '"\033c"'])
    print(field)


if __name__ == '__main__':
    from math import sin, cos, pi
    X_length = 120
    Y_length = 32
    field = BrailleField(X_length, Y_length)
    field.plot_function(func_y=lambda t: 15*(sin((t/60 - 1)*pi) + 1))
    field.plot_function(func_y=lambda t: 15)
    field.plot_function(func_x=lambda t: 59)
    update_field(field)
