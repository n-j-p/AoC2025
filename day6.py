import itertools as it
from functools import reduce
sample_data = ['123 328  51 64 ',
    ' 45 64  387 23 ',
    '  6 98  215 314',
    '*   +   *   +  ']

def get_col_indices(data):

    z=[set([i for i,x in enumerate(data[j]) if x == ' ']) for j in range(len(data))]

    all_spaces = z[0]
    for x in z[1:]:
        all_spaces = all_spaces.intersection(x)
    tt = sorted(all_spaces)
    tt.insert(0,-1)
    tt.append(len(data[0]))
    return tt

def part1(data):
    ixes = get_col_indices(data)
    split = [[row[x[0]+1:x[1]] for x in it.pairwise(ixes)] for row in data]
    # print(split)

    i = 0

    # tx = [int(n) for n in split]
    tot = 0
    for col in zip(*split):
    
        # print(col)
        ns = [int(n) for n in col[:-1]]
        # print(ns)
        if col[-1].strip() == '+':
            ans = reduce(lambda x,y: x+y, ns)
        elif col[-1].strip() == '*':
            ans = reduce(lambda x,y: x*y, ns)
        else:
            raise Exception
        
        tot += ans
    return tot
def part2(data):
    ixes = get_col_indices(data)
    split = [[row[x[0]+1:x[1]] for x in it.pairwise(ixes)] for row in data]
    # print(split)

    i = 0
    # return(split, list(zip(*split)))

    tot = 0
    for col in zip(*split):
        nstr = [''.join(y) for y in zip(*[list(x) for x in col[:-1]])]
        # print(nstr)
        ns = [int(n) for n in nstr]

        if col[-1].strip() == '+':
            ans = reduce(lambda x,y: x+y, ns)
        elif col[-1].strip() == '*':
            ans = reduce(lambda x,y: x*y, ns)
        else:
            raise Exception
        
        tot += ans
    return tot
if __name__ == '__main__':

    actual_data = open('c:/temp/day6_input.txt', 'r').read().split('\n')[:-1]

    assert part1(sample_data) == 4277556

    print(part1(actual_data))