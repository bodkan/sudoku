This repo is intended as a playground to test different optimization
options in Python (think PyPy, Cython, Numba, calling external C++ code
etc.). In no way does this claim to be a smart | fancy | efficient solution
of the sudoku puzzle. At least not yet anyway.

At the moment the program uses a simple recursion algorithm where in each
step of the recursion the program chooses to place a number in an empty square
which has the lowest number of legal possible values. In this way, the backtracking
tree is being cut down as shallow as possible, limiting the number of recursion
steps necessary to find the solution.

