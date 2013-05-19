# coding=utf-8
# Game rule see : http://www.atlas-zone.com/complex/alife/ca/ca2/page1.htm
__author__ = 'ChenKan'

import numpy
import time
import os
from termcolor import colored
from random import randint

global grid_size
global grid


# 可燃物建模
# hp - 可燃量 每次迭代消耗1点HP 为零时 熄灭
# fm - 易燃性 取值在1-9 取值为N 则周边只须要有N个已燃烧即引燃
def get_basic_object(name, is_fired, hp, fm):
    return {'name': name, 'is_fired': is_fired, 'hp': hp, 'fm': fm}


def get_stone():
    return get_basic_object('stone', False, hp=0, fm=9)


def get_wood(is_fired):
    return get_basic_object('wood', is_fired, hp=10, fm=3)


def get_withered_leaf(is_fired):
    return get_basic_object('leaf', is_fired, hp=3, fm=1)


# 在终端中执行才会有清屏效果
def clear_screen():
    os.system('clear')  # Linux / Mac
#   os.system('cls')    # Windows


# The forest to be fired
def init_grid():
    global grid_size, grid
    grid_size = 11

    # noinspection PyUnusedLocal
    grid = numpy.array([[get_withered_leaf(False) for i in range(grid_size)] for j in range(grid_size)], dtype=object)
    # setup stone
    for i in range(10):
        grid[randint(0, grid_size - 1), randint(0, grid_size - 1)] = get_stone()
    # setup wood
    for i in range(20):
        grid[randint(0, grid_size - 1), randint(0, grid_size - 1)] = get_wood(False)
    # setup fire seed
    grid[5, 5] = get_withered_leaf(True)


def update_grid():
    global grid_size, grid

    # noinspection PyUnusedLocal
    next_grid = numpy.array([[{} for i in range(grid_size)] for j in range(grid_size)], dtype=object)
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            next_grid[i, j] = update_cell(i, j)

    grid = next_grid


def update_cell(i, j):
    cell = grid[i, j]
    name = cell['name']
    is_fired = cell['is_fired']
    hp = cell['hp']
    fm = cell['fm']

    neighbor_fired_num = calculate_neighbor_fired_num(i, j)
    if is_fired:
        if hp == 1:
            is_fired = False
        hp -= 1
    else:
        if neighbor_fired_num >= fm and hp > 0:
            is_fired = True

    return get_basic_object(name, is_fired, hp, fm)


# Grid Notation
# 1 2 3
# 8 X 4
# 7 6 5
def calculate_neighbor_fired_num(i, j):
    global grid_size, grid

    if i == 0 or j == 0:
        neighbor_1 = 0
    else:
        neighbor_1 = 1 if grid[i - 1, j - 1]['is_fired'] else 0

    if i == 0:
        neighbor_2 = 0
    else:
        neighbor_2 = 1 if grid[i - 1, j]['is_fired'] else 0

    if i == 0 or j == grid_size - 1:
        neighbor_3 = 0
    else:
        neighbor_3 = 1 if grid[i - 1, j + 1]['is_fired'] else 0

    if j == grid_size - 1:
        neighbor_4 = 0
    else:
        neighbor_4 = 1 if grid[i, j + 1]['is_fired'] else 0

    if i == grid_size - 1 or j == grid_size - 1:
        neighbor_5 = 0
    else:
        neighbor_5 = 1 if grid[i + 1, j + 1]['is_fired'] else 0

    if i == grid_size - 1:
        neighbor_6 = 0
    else:
        neighbor_6 = 1 if grid[i + 1, j]['is_fired'] else 0

    if i == grid_size - 1 or j == 0:
        neighbor_7 = 0
    else:
        neighbor_7 = 1 if grid[i + 1, j - 1]['is_fired'] else 0

    if j == 0:
        neighbor_8 = 0
    else:
        neighbor_8 = 1 if grid[i, j - 1]['is_fired'] else 0

    return neighbor_1 + neighbor_2 + neighbor_3 + neighbor_4 + neighbor_5 + neighbor_6 + neighbor_7 + neighbor_8


def print_grid():
    global grid_size, grid
    clear_screen()

    # has fired - red
    # not fired - green
    # after fired - white
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            cell = grid[i, j]
            short_name = cell['name'][0].upper()
            if cell['fm'] < 9 and cell['hp'] == 0:
                print colored(short_name, 'white'),
            else:
                if cell['is_fired']:
                    print colored(short_name, 'red'),
                else:
                    print colored(short_name, 'green'),
        print ""

    print raw_input('Enter to continue')


def main():
    init_grid()
    print_grid()
    for i in range(1, 20):
#       time.sleep(1)
        update_grid()
        print_grid()
    else:
        print 'Game Over'

if __name__ == '__main__':
    main()