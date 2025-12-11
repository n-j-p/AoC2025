import tqdm
import itertools as it
import numpy as np
import math
import pdb
from collections import namedtuple

sample_data = open('day10_sample_input.txt').read().split('\n')[:-1]
actual_data = open('c:/temp/day10_input.txt').read().split('\n')[:-1]

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

Write this as an augmented matrix, and let's row-reduce it:

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
--------------

We can do the this (Gaussian reduction to echelon form) using sympy

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
    # coefficients (related to the free variables), otherwise the search
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



def isint(x):
    return abs(int(x) - x) <= 1e-12
def allints(L):
    for x in L:
        if not isint(x):
            return False
    return True

def solve_part2(row, VERBOSE=False):
    A, nonfree = reduce_to_echelon(row)
    problem_specs = parse(row)
    free = len(problem_specs.buttons) - len(nonfree)
    if free == 1:
        # This should be able to be calculated with the general method below
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
    else: # general method, number of free variables > 1 (probably usable for 1 as well)
        min_presses = 1e12
        if VERBOSE: print(f'{free} free varibles')
        free_vars = sorted(set(range(len(problem_specs.buttons))).difference(nonfree))

        free_variable_ranges = [(1,)] # intercept (constant coefficient) term in matrix equation below
        # Rather than solve the entire linear inequality problem, which we 
        # could in theory do with something
        # like Fourier–Motzkin algorithm, let's just get the maximum number
        # of button presses that makes one of the joltages too high.

        for free_var in free_vars:
            free_variable_ranges.append(range(0,min([problem_specs.joltage[i] for i,x in enumerate(problem_specs.buttons[free_var]) if x])+1))

        # We use this to get the nonfree variables from any number of free variables:
        reconstruction_matrix = np.hstack([A[:,-1], -A[:,free_vars]])
        # Drop trailing zero rows:
        while np.abs(reconstruction_matrix[-1,:]).sum() == 0:
            reconstruction_matrix = reconstruction_matrix[:-1,:]


        for b in it.product(*free_variable_ranges):
            # Now calculate the non-free variables from the quasi-feasible range
            # for the free variables:
            nonfrees = np.dot(reconstruction_matrix, b)
            if min(nonfrees) >= 0:
                if VERBOSE: print(b, 'OK', end=': ')

                # Reconstruct all variables (free & non-free) in correct order:
                allvars = np.zeros((len(problem_specs.buttons),),dtype=int)
                allvars[list(nonfree)] = nonfrees
                allvars[list(free_vars)] = b[1:]

                if allints(allvars):
                    try:
                        assert tuple(np.dot(allvars, np.array(problem_specs.buttons))) == problem_specs.joltage
                    except AssertionError:
                        # I don't know what happened here... valid values of allvars should produce the correct voltage ??!?!
                        #print('unknown')
                        continue
                    if VERBOSE: print(allvars, np.dot(allvars, np.array(problem_specs.buttons)))

                    min_presses = min(min_presses, sum(allvars))
                    pass
                else: # discard solutions involving non-integral button presses
                    if VERBOSE: print(allvars, 'non-integral')

            else: # discard solutions involving negative button presses
                if VERBOSE: print(b, nonfrees, 'negative non-free variables')
        return min_presses


def new_part2(data):
    c = 0
    for r in tqdm.tqdm(data):
        c += solve_part2(r)
    return c

if __name__ == '__main__':
    assert new_part2(sample_data) == 33
