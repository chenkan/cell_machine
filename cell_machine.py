# coding=utf-8
# Game rule see : http://www.atlas-zone.com/complex/alife/ca/ca2/page1.htm
__author__ = 'ChenKan'

import numpy
import time
# import os


global grid_size
global grid


def cls():
    # os.system(['clear', 'cls'][os.name == 'nt'])
    print "\n" * 1
    # print 1


# 0 - dead
# 1 - alive
def init_grid():
    global grid_size, grid

    grid_size = 10
    grid = numpy.zeros((grid_size, grid_size))
    grid[9] = 1
    print grid.__class__


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

    cls()
    print grid


def main():
    init_grid()
    print_grid()
    for i in range(1, 5):
        time.sleep(0.5)
        update_grid()
        print_grid()
    else:
        print 'Game Over'

if __name__ == '__main__':
    main()