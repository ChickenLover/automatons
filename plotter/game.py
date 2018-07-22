import time
import tty
import sys
import termios
from random import choice

from math import sin, pi

from plotter import *
from maze_generator import MazeGenerator


X_length = 120
Y_length = 30
speed = 1
wall_char = 'X'
path_char = '.'
player_char = '@'
finish_char = '$'


def getch():
    fd = sys.stdin.fileno()
    old_sets = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_sets)
    return ch


class Player():
    def __init__(self, field, start_point=Point(0,0), player_char='@', speed=1):
        self.position = Point(0, 0)
        self.field = field
        self.old_dot = self.field.get_dot(start_point)
        self.field.plot_dots(self.position, dot=player_char)
        self.player_char = player_char
        self.speed = speed

    def move(self, direction, step=None):
        if step is None: step = self.speed
        new_pos = Point(self.position.x, self.position.y)
        if direction == 0:
            new_pos.y = self.position.y - step
        elif direction == 1:
            new_pos.y = self.position.y + step
        elif direction == 2:
            new_pos.x = self.position.x - step
        elif direction == 3:
            new_pos.x = self.position.x + step
        if not self.field.point_in_range(new_pos) or self.field.get_dot(new_pos) == wall_char:
            return None
        self.teleport(new_pos)
    
    def teleport(self, point):
        self.field.plot_dots(self.position, dot=self.old_dot)
        self.old_dot = self.field.get_dot(point)
        self.position = point
        self.field.plot_dots(point, dot=self.player_char)
        update_field(self.field)
        

class Controller():
    def __init__(self, game):
        self.player = game.player
        self.game = game

    def start(self):
        self.game.start_game()
        while True:
            command = getch()
            if ord(command) == 3:
                return None
            if command == 's':
                self.player.move(0)
            elif command == 'w':
                self.player.move(1)
            elif command == 'a':
                self.player.move(2)
            elif command == 'd':
                self.player.move(3)
            elif command == 'r':
                self.game.start_game()
            if self.game.check_player():
                command = input('Play again?(y/n): ')
                if command == 'y' or command == 'Y':
                    self.game.start_game()
                else:
                    return None


class MazeGame():
    def __init__(self, width, height,
                 wall_char='X', path_char='.',
                 player_char='@', finish_char='$'):
        self.exit_points = [Point(0, 0), Point(width-1, 0),
                            Point(0, height-1), Point(width-1, height-1)]
        self.generator = MazeGenerator(width, height,
                                       wall_char=wall_char, path_char=path_char, finish_char=finish_char)
        self.field = self.generator.field
        self.player = Player(self.field, speed=speed)

    def make_new_maze(self):
        self.generator.generate(start_point=random_point(0, self.field.width - 1,
                                                         0, self.field.height - 1),
                                finish_point=choice(self.exit_points))

    def start_game(self):
        self.make_new_maze()
        self.start_time = time.time()
        self.player.teleport(self.generator.start)


    def get_cur_time(self):
        return time.time() - self.start_time


    def check_player(self):
        if self.player.position in self.generator.finish_neis:
            self.win()
            return True
        return False
            
    def win(self):
        self.generator.field.fill('卍')
        update_field(self.generator.field)
        print('CONGRATULATIONS!!!')
        print(open('win.txt').read())
        print('You beat the maze in {:.2f}'.format(self.get_cur_time()))

if __name__ == '__main__':
    game = MazeGame(X_length, Y_length, 
                    wall_char=wall_char, path_char=path_char,
                    player_char=player_char, finish_char=finish_char)
    controller = Controller(game)
    controller.start()
