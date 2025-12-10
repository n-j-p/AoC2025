sample_data = open('day10_sample_input.txt').read().split('\n')[:-1]
actual_data = open('c:/temp/day10_input.txt').read().split('\n')[:-1]
from collections import namedtuple
Problem = namedtuple("Problem", ['nlights', 'on', 'buttons','joltage'])
def parse(row):
    rowsp = row.split(' ')
    # print(rowsp)
    nlights = len(rowsp[0])-2
    buttons = rowsp[1:-1]
    button_tuples = [tuple([int(x) for x in b[1:-1].split(',')]) for b in buttons]
    # print(button_tuples)
    button_rows = [[1 if i in b else 0 for i in range(nlights)] for b in button_tuples]
    joltage = tuple([int(x) for x in rowsp[-1][1:-1].split(',')])
    return Problem(nlights, 
                   [i-1 for i,x in enumerate(rowsp[0]) if x == '#'],
                   button_rows, 
                   joltage)
import itertools as it
import numpy as np
def satBF(problem):
    button_matrix = np.array(problem.buttons)
    for row_indicator in it.product([0,1], repeat = button_matrix.shape[0]):
        # print(row_indicator)
        rows_on = [j for j,y in enumerate(row_indicator) if y]
        A = button_matrix[rows_on,:]
        lights_on_after_buttons_pressed = [i for i,x in enumerate(A.sum(0) % 2) if x ]
        # print(row_indicator, A, lights_on_after_buttons_pressed)
        # if np.random.random() < 0.05:
        #     import pdb
        #     pdb.set_trace()
        # print(rows_on)
        # if rows_on == [1,3]:
        #     import pdb
        #     pdb.set_trace()
        if lights_on_after_buttons_pressed == problem.on:
            # print('-----------------')
            # print(rows_on)
            yield(rows_on)
import tqdm
def part1(data):
    c = 0
    for row in tqdm.tqdm(data):
        cr = 1e12
        for x in satBF(parse(row)):
            cr = min(cr,len(x))
        # print(row)
        # print(cr)
        c += cr
    return c

if __name__ == '__main__':
    for row in sample_data:
        print(parse(row))

r'''

Part 2:

For the first problem we have button_matrix:

button_matrix = \
np.array([[0, 0, 0, 1],
       [0, 1, 0, 1],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [1, 0, 1, 0],
       [1, 1, 0, 0]])

And the target joltages

target_joltages = \
np.array([3, 5, 4, 7])

One solution is 

soln = \
    [1,3,0,3,1,2] 

which is the button count array (the example
given on the problem page).

np.dot(soln, button_matrix), i.e. as a matrix equation:

[1,3,0,3,1,2]   *    [0, 0, 0, 1]     =    [3, 5, 4, 7]
                     [0, 1, 0, 1]          
                     [0, 0, 1, 0]          
                     [0, 0, 1, 1]          
                     [1, 0, 1, 0]
                     [1, 1, 0, 0]    

(1,6) X (6,4)  = (1,4)

Or transposed:

[0, 0, 0, 0, 1, 1]  [1]  =  [3]
[0, 1, 0, 0, 0, 1]  [3]     [5]
[0, 0, 1, 1, 1, 0]  [0]     [4]
[1, 1, 0, 1, 0, 0]  [3]     [7]
                    [1]
                    [2]

RR:
0 0 0 0 1 1 | 3
0 1 0 0 0 1 | 5
0 0 1 1 1 0 | 4
1 1 0 1 0 0 | 7

rearrange rows:
1 1 0 1 0 0 | 7
0 1 0 0 0 1 | 5
0 0 1 1 1 0 | 4
0 0 0 0 1 1 | 3

R1 = R1 - R2:

1 0 0 1 0 -1 | 2
0 1 0 0 0  1 | 5
0 0 1 1 1  0 | 4
0 0 0 0 1  1 | 3

R3 = R3 - R4:

1 0 0 1 0 -1 | 2
0 1 0 0 0  1 | 5
0 0 1 1 0 -1 | 1
0 0 0 0 1  1 | 3

Giving us:

A + D - F = 2
B + F = 5
C + D - F = 1
E + F = 3

D, F free variables

i.e. we could set D, F = 0 and then
A = 2, B = 5, C = 1, E = 3

or set D = 1, F = 1:

A = 2
B = 4
C = 1
E = 2

so that

soln2 = [2,5,1,0,3,0]
soln3 = [2,4,1,1,2,1]

are both solutions.

However both of these require 11 button presses.

Now, given a set of equations with free variables, e.g.:


A + D - F = 2
B + F = 5
C + D - F = 1
E + F = 3

(or equivalent augmented, reduced matrix):

1 0 0 1 0 -1 | 2
0 1 0 0 0  1 | 5
0 0 1 1 0 -1 | 1
0 0 0 0 1  1 | 3

valid solutions are for non-negative free variables. If there are no negative
coefficients, any solution is valid but we should take free variables all 
equal to zero.

Total button presses are equal to


----
A + D - F = 2
B + F = 5
C + D - F = 1
E + F = 3
----

A = 2 - D + F
B = 5 - F
C = 1 - D + F
E = 3 - F

so f(D,F) = 11 - D + F
subject to D, F >= 0
also B >= 0 or 5 - F >= 0, F <= 5
C >= 0 or 1 - D + F >= 0, 


--------------

We can do the first step (Gaussian reduction to echelon form using sympy)

'''

from sympy import Matrix
def reduce_to_echelon(row):
    parsed = parse(row)
    augmented = np.hstack([np.array(parsed.buttons).T,
                           np.array(parsed.joltage)[:,np.newaxis]])
    return Matrix(augmented).rref()

def part2(data):
    frees = []
    for i, row in enumerate(data):
        A, nonfree = reduce_to_echelon(row)
        free = A.shape[1]-1 - len(nonfree)
        frees.append(free)
        print(f'{i+1}: {A.shape[1]-1} buttons, {free} free variables')
    return frees

r'''
Now, if there are no free variables, there is only one solution, e.g. for
actual_data[0] we get:

(Matrix([
 [1, 0, 0, 0, 0,  9],
 [0, 1, 0, 0, 0,  4],
 [0, 0, 1, 0, 0, 17],
 [0, 0, 0, 1, 0,  6],
 [0, 0, 0, 0, 1, 11],
 [0, 0, 0, 0, 0,  0],
 [0, 0, 0, 0, 0,  0]]),
 (0, 1, 2, 3, 4))

Then the solution is [9,4,17,6,11]

Check:

np.dot([9,4,17,6,11],np.array(parse(actual_data[0]).buttons))

is equal to the required joltage.

Otherwise we need to work out the feasible search space. All button presses
need to be non-negative integers, so the free variables are all >= 0.

However, for large enough values of the free variables, the joltage solution
will require negative button presses for (some of) the nonfree variables.

For one free variable we can just search through it.count(0)
'''

def _feasible1(A, nonfree):
    nfree = A.shape[1]-1 - len(nonfree)
    assert nfree == 1

    # Remove any zero rows from A:
    Ac = np.array(A).copy()
    for _ in range(len(Ac)):
        if sum(abs(Ac[-1,:])) == 0:
            Ac = Ac[:-1,:]
    print(A)
    print(Ac)

    free_vars = sorted(set(range(A.shape[1]-1)).difference(nonfree))

    B = np.hstack([Ac[:,[A.shape[1]-1]], 
                   -Ac[:,free_vars]])

    # Assume that the nonfree variable equations contain some negative
    # coefficients (relatd to the free variables), otherwise the search
    # space is infinite...
    assert np.min(B) < 0 

    return Ac, free_vars, B


r'''

for sample_data[2] we get:

array([[6, -1],
        [-1, 1],
        [5, 0]], dtype=object))
which corresponds to:

A = 6 - D
B = -1 + D
C = 5
D free

here A >= 0 means 6 - D >= 0 or D <= 6
and  B >= 0 means -1 + D >= 0 or D >= 1

so feasible range for D is [1,6]

'''
def feasible1(A, nonfree):
    nfree = A.shape[1]-1 - len(nonfree)
    assert nfree == 1

    # Remove any zero rows from A:
    Ac = np.array(A).copy()
    for _ in range(len(Ac)):
        if sum(abs(Ac[-1,:])) == 0:
            Ac = Ac[:-1,:]
    # print(A)
    # print(Ac)

    free_vars = sorted(set(range(A.shape[1]-1)).difference(nonfree))

    B = np.hstack([Ac[:,[A.shape[1]-1]], 
                   -Ac[:,free_vars]])

    # Assume that the nonfree variable equations contain some negative
    # coefficients (relatd to the free variables), otherwise the search
    # space is infinite...
    assert np.min(B) < 0 

    mins = []
    maxes = []
    for r in B:
        if r[1] == 0:
            # This doesn't correspond to a constraint on F
            continue
        elif r[1] < 0:
            maxes.append(-r[0] / r[1])
        else:
            mins.append(-r[0] / r[1])
    if len(mins) == 0:
        return 0, min(maxes), B
    else:
        return max(0,max(mins)), min(maxes), B

def get_all_feasible(data):
    for i, row in enumerate(data):
        A, nonfree = reduce_to_echelon(row)
        free = A.shape[1]-1 - len(nonfree)
        if free == 1:
            print(f'row {i+1}, {feasible1(A,nonfree)}')
        else:
            print(f'row {i+1}, {free} free variables')

def isint(x):
    return abs(int(x) - x) <= 1e-12
def allints(L):
    for x in L:
        if not isint(x):
            return False
    return True
import math
def solve_part2(row, VERBOSE=False):
    A, nonfree = reduce_to_echelon(row)
    free = A.shape[1]-1 - len(nonfree)
    if free == 1:
        min_presses = 1e12
        mn, mx, B = feasible1(A,nonfree)
        for F in range(math.ceil(mn), math.floor(mx)+1):
            nonfrees = np.dot(B, [1,F])
            if allints(nonfrees):
                if VERBOSE: print(F, nonfrees, sum(nonfrees) + F)
                min_presses = min(min_presses, sum(nonfrees) + F)
        return min_presses
    elif free == 0:
        return np.sum(A[:,-1])
    else:
        print(f'{free} free varibles')

