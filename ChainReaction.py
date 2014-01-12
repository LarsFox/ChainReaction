#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import random

import pygame
from pygame.locals import *

# =====================================================================
class Game(object):
    def __init__(self, GAME_NAME, WINDOW_SIZE, ROWS, COLUMNS):
        pygame.init()
        pygame.display.set_caption(GAME_NAME)
        pygame.display.set_icon(ICON)

        self.screen = pygame.display.set_mode(WINDOW_SIZE)

        def form_moleculas(rows, columns):
            array = []
            for x in xrange(rows):
                array.append([])

                for y in xrange(columns):
                    array[x].append(Molecula(x, y))

            return array

        self.moleculas = form_moleculas(ROWS, COLUMNS)
        self.indexes = []

    def start(self):
        while MAINLOOP:
            self.display()
            self.key_controller()

            if not self.indexes:
                self.moleculas_clickable = True
                self.record = 0
            else:
                new_indexes = []
                for index in self.indexes:
                    molecula = self.moleculas[index[0]][index[1]]
                    molecula.move()
                    self.record += 1

                    new_indexes += self.get_neighbours(molecula)

                new_indexes = list(set(new_indexes))
                #print new_indexes
                print self.record
                self.indexes = new_indexes

                time.sleep(0.5)

        pygame.quit()

    def get_neighbours(self, molecula):
        # Up, Right, Down, Left: clockwise
        row = molecula.row
        column = molecula.column
        bond = molecula.bond

        result = []

        def check_up():
            if row:
                up = self.moleculas[row-1][column]
                if up.bond == 1 or up.bond == 2:
                    result.append(up.index)

        def check_right():
            if column != MOLECULAS_COLUMNS-1:
                right = self.moleculas[row][column+1]
                if right.bond == 2 or right.bond == 3:
                    result.append(right.index)

        def check_down():
            if row != MOLECULAS_ROWS-1:
                down = self.moleculas[row+1][column]
                if down.bond == 3 or not down.bond:
                    result.append(down.index)

        def check_left():
            if column:
                left = self.moleculas[row][column-1]
                if not left.bond or left.bond == 1:
                    result.append(left.index)

        if not bond:
            check_up()
            check_right()

        elif bond == 1:
            check_right()
            check_down()

        elif bond == 2:
            check_down()
            check_left()

        elif bond == 3:
            check_left()
            check_up()

        return result

    def display(self):
        def draw_moleculas():
            x, y = STARTX, STARTY

            for row in self.moleculas:
                for molecula in row:
                    self.screen.blit(MOLECULAS_IMAGES[molecula.bond], (x, y))
                    molecula.rect = pygame.Rect(
                        (x, y), (MOLECULA_IMG_SIDE, MOLECULA_IMG_SIDE))
                    x += MOLECULA_IMG_SIDE

                x = STARTX
                y += MOLECULA_IMG_SIDE


        tickFPS = CLOCK.tick(FPS)
        self.screen.fill(PALETTE['Background'])

        draw_moleculas()

        pygame.display.update()

    def key_controller(self):
        def click_moleculas():            
            for row in self.moleculas:
                for molecula in row:
                    if molecula.rect.collidepoint(event.pos):
                        self.indexes = [molecula.index]

                        self.moleculas_clickable = False

        for event in pygame.event.get():
            if event.type == QUIT:
                MAINLOOP = False
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.moleculas_clickable:
                    click_moleculas()


class Molecula(object):
    def __init__(self, row, column):
        self.bond = int(random.random() * MOLECULA_STATES)
        self.row = row
        self.column = column

    @property
    def index(self):
        return (self.row, self.column)

    def draw_spin(self):
        pass

    def move(self):
        self.bond += 1
        if self.bond == 4:
            self.bond = 0

    #def __str__(self):
        #return STR_MOLECULAS[self.bond]


# =====================================================================

GAME_NAME = 'Chain Reaction'
WINDOW_SIZE = (800, 600)

PALETTE = {
    'Background':   (216, 209, 232)
}
#STR_MOLECULAS = ['b', 'p', 'q', 'd']

MOLECULAS_ROWS = 16
MOLECULAS_COLUMNS = 16
MOLECULA_STATES = 4

MOLECULAS_IMAGES = [
    pygame.image.load('0.png'),
    pygame.image.load('1.png'),
    pygame.image.load('2.png'),
    pygame.image.load('3.png')
]
ICON = MOLECULAS_IMAGES[random.randint(0, 3)]

STARTX, STARTY = 100, 50
MOLECULA_IMG_SIDE = 15

MAINLOOP = True
CLOCK = pygame.time.Clock()
FPS = 30

game = Game(GAME_NAME, WINDOW_SIZE, MOLECULAS_ROWS, MOLECULAS_COLUMNS)

game.start()
'''
test = game.form_moleculas(MOLECULAS_ROWS, MOLECULAS_COLUMNS)

def print_moleculas(array):
    for item in array:
        for jtem in item:
            print jtem,
        print ''

indexes = [(0, 0)]

for x in xrange(10):
    new_indexes = []
    for index in indexes:
        if EXCEPTION in index: continue
        if EXCEPTION in index: continue
        if MOLECULAS_ROWS in index: continue
        if MOLECULAS_COLUMNS in index: continue

        molecula = test[index[0]][index[1]]
        molecula.move()

        new_indexes += molecula.get_neighbours()


    print new_indexes
    new_indexes = list(set(new_indexes))
    print new_indexes
    indexes = new_indexes

    print_moleculas(test)

# массив с индексами молекул, которые должны были повернуться
# их поворот
# получение новых молекул, заполнение ими массива list(set(ARRAY))
# while not ARRAY

#game = Game(GAME_NAME, WINDOW_SIZE)
#game.start()
'''
'''
molecula = test[2][2]

def test_connections(molecula):
    for x in xrange(4):
        print molecula,
        nei = molecula.get_neighbours()
        for item in nei:
            print test[item[0]][item[1]],

        print ''
        molecula.move()
        '''

#indexes = raw_input('> ') # does not work inside the Sublime
#indexes = [(indexes.split())]
