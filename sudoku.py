import argparse
import math
import random
from itertools import chain

EMPTY = None
SUDOKU_SIZE = 9
SQUARE_SIZE = int(math.sqrt(SUDOKU_SIZE))
ALL = set(range(1, SUDOKU_SIZE + 1))


def pretty_print(sudoku):
    '''Print out the sudoku data structure in a readable format.'''
    ROW_SEP = '-' * (SUDOKU_SIZE + SQUARE_SIZE + 1)
    COL_SEP = '|'

    for i, row in enumerate(sudoku):
        # print the vertical separator
        if i % SQUARE_SIZE == 0: print(ROW_SEP)

        for j, col in enumerate(row):
            if j % SQUARE_SIZE == 0: print(COL_SEP, end='')
            print(' ' if not sudoku[i][j] else sudoku[i][j], end='')
        print(COL_SEP)
    print(ROW_SEP)


def read_sudoku(filepath):
    '''Read sudoku from a file in the form of list of lists'''
    f = open(filepath, 'r')
    return [[EMPTY if n == '0' else int(n) for n in row.strip()] for row in f]


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
    # return the position with the smallest set of valid options
    return sorted(options, key=lambda o: len(o[2]))[0]


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solve a given sudoku puzzle and print'
        ' the solution to the terminal')
    parser.add_argument('--input', help='File with the input puzzle (NxN'
        ' matrix containing numbers 0-9 with 0 indicating a missing value)',
        required=True)
    args = parser.parse_args()

    solved_sudoku = solve(read_sudoku(args.input))
    pretty_print(solved_sudoku)
