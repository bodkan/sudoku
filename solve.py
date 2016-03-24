import argparse
import sys
import math
import random
from itertools import chain


EMPTY = None
SUDOKU_SIZE = 9
SQUARE_SIZE = 3
ALL = set(range(1, SUDOKU_SIZE + 1))


def row_values(i, sudoku):
    '''Get a set of already taken values in the given row.'''
    return set(n for n in sudoku[i] if n is not EMPTY)


def col_values(j, sudoku):
    '''Get a set of already taken values in the given column.'''
    return set(sudoku[i][j] for i in range(SUDOKU_SIZE)
                            if sudoku[i][j] is not EMPTY)


def square_values(i, j, sudoku):
    '''Get a set of already taken values in the square where the position
    (i,j) falls into.
    '''
    # coordinate of the upper left corner of the square
    upper_i = (i // SQUARE_SIZE) * SQUARE_SIZE
    upper_j = (j // SQUARE_SIZE) * SQUARE_SIZE

    # get values of occupied positions in the square
    return set(sudoku[k][l] for k in range(upper_i, upper_i + SQUARE_SIZE)
                            for l in range(upper_j, upper_j + SQUARE_SIZE)
                            if sudoku[k][l] is not EMPTY)


def free_values(i, j, sudoku):
    '''Return a set of values that can be legally placed in a given
    position of the sudoku.
    '''
    return ALL - (row_values(i, sudoku) |
                  col_values(j, sudoku) |
                  square_values(i, j, sudoku))


def solved(sudoku):
    '''Is the sudoku completely solved?'''
    # the puzzle is solved if all positions are filled
    return all(chain.from_iterable(sudoku))


def next_to_fill(sudoku):
    '''Find a position with the lowest number of possible valid options
    (to cut down the recursion tree) and return its coordinates along
    with the list of options.
    '''
    # accumulate the set of valid options at each empty position
    options = [(i, j, free_values(i, j, sudoku)) for i in range(SUDOKU_SIZE)
                                                 for j in range(SUDOKU_SIZE)
                                                 if sudoku[i][j] is EMPTY]

    # what is the lowest number of free values at any empty position?
    min_opts = min(len(o[2]) for o in options)

    # return the position with the smallest set of valid options
    # (if there are multiple options, choose a random one)
    return random.choice([o for o in options if len(o[2]) == min_opts])


def solve(sudoku):
    '''Recursively solve the sudoku puzzle.'''
    # if the solution as been reached propagate it 'upwards'
    if solved(sudoku):
        return sudoku
    else:
        # find the next best position and its valid values
        i, j, options = next_to_fill(sudoku)
        for o in options:
            sudoku[i][j] = o
            # the solution has been found => propagate it back
            if solve(sudoku): return sudoku
        else:
            # none of the options lead to a solution
            #   => remove them and backtrack
            sudoku[i][j] = EMPTY
            return


def init_empty():
    '''Initialize an empty sudoku.'''
    return [[EMPTY] * SUDOKU_SIZE for _ in range(SUDOKU_SIZE)]


def generate():
    '''Generate a new puzzle by solving an empty one.'''
    s = init_empty()
    return solve(s)


def pretty_print(sudoku, handle=sys.stdout):
    '''Print out the sudoku data structure in a readable format.'''
    ROW_SEP = '-' * (SUDOKU_SIZE + SQUARE_SIZE + 1)
    COL_SEP = '|'

    for i, row in enumerate(sudoku):
        # print the vertical separator
        if i % SQUARE_SIZE == 0: print(ROW_SEP, file=handle)

        for j, col in enumerate(row):
            if j % SQUARE_SIZE == 0: print(COL_SEP, end='', file=handle)
            print(' ' if not sudoku[i][j] else sudoku[i][j], end='', file=handle)
        print(COL_SEP, file=handle)
    print(ROW_SEP, file=handle)


def read_sudoku(filepath):
    '''Read sudoku from a file in the form of list of lists'''
    f = open(filepath, 'r')
    return [[EMPTY if n == '0' else int(n) for n in row.strip()] for row in f]


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solve a given sudoku puzzle and print'
        ' the solution to the terminal. Alternatively, generate a new puzzle.')
    parser.add_argument('--solve', action='store_true')
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--file', help='File with with the puzzle (NxN'
        ' matrix containing numbers 0-9 with 0 indicating a missing value)',
        required=True)
    args = parser.parse_args()

    if args.solve:
        sudoku = solve(read_sudoku(args.file))
        pretty_print(sudoku)
    else:
        sudoku = generate()
        with open(args.file, 'w') as output:
            pretty_print(sudoku, output)
 
