import curses
import random

class Snake(object):

    def __init__(self, x, y, window):
        pass
        # initialize snake:
        # - create head
        # - create body
        # - set starting x, y position

    def eat_food(self, food):
        pass
        # remove food
        # stretch body
        # add score
        # make the game faster

    def update(self):
        pass
        # update snake location (move the snake)

    def render(self):
        pass
        # draw the snake in the console using curses

    def move(self):
        pass
        # move up down left right.

class Body(object):
    def __init__(self, x, y, char='#'):
        self.x = x
        self.y = y
        self.char = char

    @property
    def coor(self):
        return self.x, self.y




class Food(object):
    def __init__(self, window, char='*'):
        pass
        # set random x, y position

    def render(self):
        pass
        # draw food to console

    def randomize(self):
        pass
        # randomize x, y position



def main():
    while True:
        pass
        # clear screen
        # display the snake
        # display the food
        # display the score
        # listen to keypress event
        # respond to keypress event
        # stop the game if the head hits the body (eat itself)


if __name__ == "__main__":
    main()