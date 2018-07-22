import time
from random import choice, shuffle
from math import ceil, sqrt

from plotter import *
#from game import getch


X_length = 30
Y_length = 15


class MazeGenerator():
    def __init__(self, width, height,
                 wall_char='X', path_char='.', finish_char='$'):
        self.field = Field(width, height, ' ', wall_char)
        self.width = width
        self.height = height
        self.wall_char = wall_char
        self.path_char = path_char
        self.finish_char = finish_char
        self.rat_char = 'R'
        self.moving_back = False


    def init_maze(self, start_point, finish_point):
        if not start_point: start_point = Point()
        if not finish_point: finish_point = Point(self.width-1, self.height-1)
        self.start = start_point
        self.finish_neis = list(self.field.get_neighbours(finish_point))
        self.field.fill(' ')
        self.field.plot_dots(self.start, dot=self.path_char)
        self.field.plot_dots(*filter(self.field.point_in_range,
                               [Point(self.start.x + j, self.start.y + i)\
                                       for i in [-1, 1]\
                                       for j in [-1, 1]]),
                       dot=self.wall_char)
        self.moves = [self.start]
        self.cur_pos = self.start


    def get_valid_move(self):
        paths = self.get_clear_paths()
        if paths: return choice(paths)


    def get_clear_paths(self):
        return list(filter(lambda p: not self.field.if_dot(p),
                           self.field.get_close_neighbours(self.cur_pos)))


    def get_clear_neis(self):
        return list(filter(lambda p: not self.field.if_dot(p),
                           self.field.get_neighbours(self.cur_pos)))


    def step_back(self):
        try:
            return self.moves.pop()
        except IndexError:
            return None


    def build_walls(self):
        clear_paths = self.get_clear_paths()
        shuffle(clear_paths)
        for _ in range(ceil(len(clear_paths)/2)):
            self.field.plot_dots(clear_paths.pop())


    def check_for_turns(self, new_pos):
        try:
            old_pos = self.moves[-2]
            diff = new_pos - old_pos
            if abs(diff) == sqrt(2):
                p1 = Point(old_pos.x + diff.x, old_pos.y)
                p2 = Point(old_pos.x, old_pos.y + diff.y)
                if p1 != self.cur_pos:
                    self.field.plot_dots(p1)
                else:
                    self.field.plot_dots(p2)
        except IndexError: 
            pass


    def make_move(self, new_pos):
        self.field.plot_dots(new_pos, dot=self.rat_char)
        self.check_for_turns(new_pos)
        self.build_walls()
        self.cur_pos = new_pos
        self.moves.append(new_pos)


    def generate(self, start_point=None, finish_point=None):
        self.init_maze(start_point, finish_point)
        i = 0
        while self.cur_pos not in self.finish_neis:
            i += 1
            self.field.plot_dots(self.cur_pos, dot=self.path_char)
            if self.moving_back:
                back_pos = self.step_back()
                if not back_pos:
                    self.moving_back = False
                    self.init_maze(start_point, finish_point)
                    continue
                self.field.plot_dots(back_pos, dot='B')
            new_pos = self.get_valid_move()
            if new_pos:
                if self.moving_back:
                    self.field.plot_dots(back_pos, dot=self.path_char)
                    self.moving_back = False
                self.make_move(new_pos)
            else:
                if not self.moving_back: self.moving_back = True
                else: self.cur_pos = back_pos
            if not i%10: update_field(self.field)
            #time.sleep(0.1)
            #update_field(self.field)
            #if ord(getch()) == 3: break
        self.field.plot_dots(self.cur_pos, dot=self.path_char)
        for point in self.finish_neis:
            self.field.plot_dots(point, dot=self.finish_char)
        for point in self.field.find_dots(' '):
            self.field.plot_dots(point, dot=choice([self.path_char] + [self.wall_char] * 3))
            #update_field(self.field)
            #time.sleep(0.1)

        

if __name__ == '__main__':
    generator = MazeGenerator(X_length, Y_length)
    generator.generate()
