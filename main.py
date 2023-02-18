import numpy as np
import pyautogui
import imutils
import cv2
from math import floor, ceil
from time import sleep

start_h = 169
start_w = 1296
dimension = (16, 30)
rows = dimension[0]
cols = dimension[1]
pixel_size = 30

reference_nothing = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/nothing.png')), cv2.COLOR_BGR2GRAY)
reference_blank = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/blank.png')), cv2.COLOR_BGR2GRAY)
reference_flag = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/flag.png')), cv2.COLOR_BGR2GRAY)

reference_1 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/1.png')), cv2.COLOR_BGR2GRAY)
reference_2 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/2.png')), cv2.COLOR_BGR2GRAY)
reference_3 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/3.png')), cv2.COLOR_BGR2GRAY)
reference_4 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/4.png')), cv2.COLOR_BGR2GRAY)
reference_5 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/5.png')), cv2.COLOR_BGR2GRAY)
reference_6 = cv2.cvtColor(np.array(cv2.imread(
    '/Users/tarioyou/code/minesweeper/references/6.png')), cv2.COLOR_BGR2GRAY)
# reference_7
# reference_8

references = [reference_nothing, reference_blank, reference_flag, reference_1,
              reference_2, reference_3, reference_4, reference_5, reference_6]
ref_names = ['#', ' ', 'f', '1', '2', '3', '4', '5', '6']


class c:
    blue = '\x1b[0;37;44m'
    red = '\x1b[0;37;41m'
    endc = '\x1b[0m'


directions = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse


def read_grid():
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    h, w = image.shape
    image = image[start_h:start_h+dimension[0]
                  * 30, start_w:w-366]  # monitor top right

    # cv2.imshow('', image)
    # cv2.waitKey(0)

    h, w = image.shape
    pixel_size = h/16
    grid = []
    for y in range(dimension[0]):
        row = []
        for x in range(dimension[1]):
            start_y = floor(y*pixel_size)
            start_x = floor(x*pixel_size)
            cell = image[start_y:start_y+28,
                         start_x:start_x+28]

            mses = []
            # print(cell.shape)
            for i in range(len(ref_names)):
                m = mse(cell, references[i])
                # print(f'{ref_names[i]}\t{m}')

                if (i == 0 or i == 1) and m <= 5.0:
                    m += 4

                mses.append(m)
            predicted = ref_names[mses.index(min(mses))]
            # print(f'\n{(y,x)}\tpredicted = \'{predicted}\'\n')

            # cv2.imshow('cell', cell)
            # cv2.waitKey(0)

            row.append(predicted)

            cv2.imwrite(
                f'/Users/tarioyou/code/minesweeper/references_buffer/cell{y}_{x}.png', cell)

        grid.append(row)
    return grid


def display_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end=' ')
        print()


def get_m1_m2(grid):
    m1 = []
    m2 = []
    for y in range(0, dimension[0]):
        for x in range(0, dimension[1]):
            if grid[y][x].isdigit():
                flags = []
                unclicked = []
                for i in range(len(directions)):
                    y_dev = y+directions[i][0]
                    x_dev = x+directions[i][1]
                    if not (x_dev >= 0 and x_dev < dimension[1] and y_dev >= 0 and y_dev < dimension[0]):
                        continue
                    border_cell = grid[y_dev][x_dev]
                    if border_cell == 'f':
                        # print(f'{border_cell = }\t{(y_dev, x_dev)}\t{i}')
                        flags.append((y_dev, x_dev))
                    elif border_cell == ' ':
                        unclicked.append((y_dev, x_dev))
                # print(f'{(y, x)}  \t{grid[y][x]}\tflags = {len(flags)}')
                if len(flags) + len(unclicked) == int(grid[y][x]):
                    m2 += unclicked
                elif len(flags) == int(grid[y][x]):
                    m1 += unclicked
    return m1, m2


def execute_m2(m2):
    for b in m2:
        x_coord = start_w+int(b[1]*pixel_size)+15
        y_coord = start_h+int(b[0]*pixel_size)+15
        pyautogui.moveTo(x=x_coord, y=y_coord)
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')


def execute_m1(m1):
    for b in m1:
        x_coord = start_w+int(b[1]*pixel_size)+15
        y_coord = start_h+int(b[0]*pixel_size)+15
        pyautogui.moveTo(x=x_coord, y=y_coord)
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')


def display_moves(grid, m1, m2):
    for y in range(dimension[0]):
        for x in range(dimension[1]):
            cell = grid[y][x]
            if (y, x) in m1:
                print(f'{c.blue}{cell}{c.endc}', end=' ')
            elif (y, x) in m2:
                print(f'{c.red}{cell}{c.endc}', end=' ')
            else:
                print(cell, end=' ')
        print()
    print()


def check_1_1(grid, m1, m2):
    # first row
    for x in range(cols):
        if [grid[0][x], grid[1][x], grid[2][x]] == ['1', '1', '1']:
            if x-1 >= 0 and [grid[0][x-1], grid[1][x-1], grid[2][x-1]] == [' ', ' ', ' ']:
                m1.append((2, x-1))
            elif x+1 < cols and [grid[0][x+1], grid[1][x+1], grid[2][x+1]] == [' ', ' ', ' ']:
                m1.append((2, x+1))

    # last row
    for x in range(cols):
        if [grid[rows-1][x], grid[rows-2][x], grid[rows-3][x]] == ['1', '1', '1']:
            if x-1 >= 0 and [grid[rows-1][x-1], grid[rows-2][x-1], grid[rows-3][x-1]] == [' ', ' ', ' ']:
                m1.append((rows-3, x-1))
            elif x+1 < cols and [grid[rows-1][x+1], grid[rows-2][x+1], grid[rows-3][x+1]] == [' ', ' ', ' ']:
                m1.append((rows-3, x+1))

    # first column
    for y in range(rows):
        if [grid[y][0], grid[y][1], grid[y][2]] == ['1', '1', '1']:
            if y-1 >= 0 and [grid[y+1][0], grid[y+1][1], grid[y+1][2]] == [' ', ' ', ' ']:
                m1.append((y+1, 2))
            elif y+1 < rows and [grid[y-1][0], grid[y-1][1], grid[y-1][2]] == [' ', ' ', ' ']:
                m1.append((y-1, 2))

    # last column
    for y in range(rows):
        if [grid[y][cols-1], grid[y][cols-2], grid[y][cols-3]] == ['1', '1', '1']:
            if y-1 >= 0 and [grid[y+1][cols-1], grid[y+1][cols-2], grid[y+1][cols-3]] == [' ', ' ', ' ']:
                m1.append((y+1, cols-3))
            elif y+1 < rows and [grid[y-1][cols-1], grid[y-1][cols-2], grid[y-1][cols-3]] == [' ', ' ', ' ']:
                m1.append((y-1, cols-3))

    return m1, m2


def check_patterns(grid, m1, m2):
    m1, m2 = check_1_1(grid, m1, m2)

    return m1, m2


if __name__ == "__main__":
    # grid = read_grid()
    # display_grid(grid)
    # quit()

    # grid = read_grid()
    # m1, m2 = check_patterns(grid, [], [])
    # print(m1)

    # display_moves(grid, m1, m2)

    # input('enter?')
    # pyautogui.click(start_w, start_h-20) # focus on minesweeper window
    # execute_m1(m1)
    # execute_m2(m2)

    # quit()

    m1 = [1]
    m2 = []

    while m1 != [] or m2 != []:
        pyautogui.click(start_w-400, start_h-20)  # chance to quit
        grid = read_grid()
        m1, m2 = get_m1_m2(grid)
        m1, m2 = check_patterns(grid, m1, m2)
        m1 = list(dict.fromkeys(m1))
        m2 = list(dict.fromkeys(m2))
        display_moves(grid, m1, m2)
        # input('enter to execute move')
        pyautogui.click(start_w, start_h-20)  # focus on minesweeper window
        execute_m1(m1)
        execute_m2(m2)

    '''
    w = 30
    h = 16
    '''
