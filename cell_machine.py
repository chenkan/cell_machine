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

    next_tick_grid = numpy.zeros((grid_size, grid_size))
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            next_tick_grid[i, j] = get_cell_new_status(i, j)
    grid = next_tick_grid


def get_cell_new_status(i, j):
    neighbor_alive_num = calculate_neighbor_alive_num(i, j)
    if grid[i, j] == 1 and (neighbor_alive_num == 2 or neighbor_alive_num == 3):
        return 1
    if grid[i, j] == 0 and (neighbor_alive_num == 3):
        return 1
    return 0


# Grid Notation
# 1 2 3
# 8 X 4
# 7 6 5
def calculate_neighbor_alive_num(i, j):
    global grid_size, grid

    if i == 0 or j == 0:
        neighbor_1 = 0
    else:
        neighbor_1 = grid[i - 1, j - 1]

    if i == 0:
        neighbor_2 = 0
    else:
        neighbor_2 = grid[i - 1, j]

    if i == 0 or j == grid_size - 1:
        neighbor_3 = 0
    else:
        neighbor_3 = grid[i - 1, j + 1]

    if j == grid_size - 1:
        neighbor_4 = 0
    else:
        neighbor_4 = grid[i, j + 1]

    if i == grid_size - 1 or j == grid_size - 1:
        neighbor_5 = 0
    else:
        neighbor_5 = grid[i + 1, j + 1]

    if i == grid_size - 1:
        neighbor_6 = 0
    else:
        neighbor_6 = grid[i + 1, j]

    if i == grid_size - 1 or j == 0:
        neighbor_7 = 0
    else:
        neighbor_7 = grid[i + 1, j - 1]

    if j == 0:
        neighbor_8 = 0
    else:
        neighbor_8 = grid[i, j - 1]

    return neighbor_1 + neighbor_2 + neighbor_3 + neighbor_4 + neighbor_5 + neighbor_6 + neighbor_7 + neighbor_8


def print_grid():
    global grid_size, grid
    clear_screen()

    # has fired - red
    # not fired - green
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            short_name = grid[i, j]['name'][0].upper()
            if grid[i, j]['is_fired']:
                print colored(short_name, 'red'),
            else:
                print colored(short_name, 'green'),
        print ""


def main():
    init_grid()
    print_grid()
    for i in range(1, 100):
        time.sleep(0.1)
        update_grid()
        print_grid()
    else:
        print 'Game Over'

if __name__ == '__main__':
    main()