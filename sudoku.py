import math

EMPTY = None
SUDOKU_SIZE = 9
SQUARE_SIZE = int(math.sqrt(SUDOKU_SIZE))


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
