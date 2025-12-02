sample_data = '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,'+\
    '1698522-1698528,446443-446449,38593856-38593862,565653-565659,'+\
        '824824821-824824827,2121212118-2121212124'

import itertools as it

# Adapted from palindrome_generator from PE36.py
def invalid_generator():
    ndigits = 2
    while True:
        prev = []
        for x in range(pow(10,ndigits//2-1), 
                    pow(10,ndigits//2)):
            nxt = str(x) + str(x)
            prev.append(nxt)
            yield int(nxt)
        ndigits += 2


def part1(data):
    r'''Construct a list of invalid numbers up to the maximum called for
    in the problem specs.
    
    Then we iterate through the ranges given and identify which invalid
    numbers are in each range'''
    ranges = data.split(',')
    LR =  [[int(x) for x in r.split('-')] for r in ranges]
    LRs = sorted(LR, key = lambda x: x[1])

    all_invalids = list(it.takewhile(lambda x: x < LRs[-1][1],
                                     invalid_generator()))

    invalid_IDs = {}
    for r in LRs:
        invalid_IDs[tuple(r)] = []
        for x in all_invalids:
            if x > r[1]:
                break
            if x >= r[0]:
                invalid_IDs[tuple(r)].append(x)

    return invalid_IDs

def invalid2(D):
    r'''Type-2 invalid numbers with D digits'''
    if D == 1:
        return []
    
    invalids = []
    # Iterate through proper divisors of D
    for n in it.count(1):
        d,r = divmod(D, n)
        if d == 1:
            # No more proper divisors 
            break

        if r == 0: # i.e. n is a divisor of D
            # If n is say 2, 
            # rng will be 10-99:
            lo = 10**(n-1)
            hi = 10**n - 1
            rng = range(lo, hi+1)

            # Now just construct d copies of each number in rng:
            invalids += [int(str(x) * d) for x in rng]
    # We get duplicates 6666 = 6.6.6.6 and 66.66
    # hence use "set" to get uniques, and sort:
    return sorted(set(invalids))

def part2(data):
    ranges = data.split(',')
    LR =  [[int(x) for x in r.split('-')] for r in ranges]
    LRs = sorted(LR, key = lambda x: x[1])

    maxD = len(str(LRs[-1][1])) 
    
    all_invalids = []
    for d in range(1, maxD+1):
        all_invalids += invalid2(d)

    invalid_IDs = {}
    for r in LRs:
        invalid_IDs[tuple(r)] = []
        for x in all_invalids:
            if x > r[1]:
                break
            if x >= r[0]:
                invalid_IDs[tuple(r)].append(x)



    return invalid_IDs

if __name__ == '__main__':
    fpath = 'C:/temp/day2_input.txt'
    input_data = open(fpath).read().split('\n')[0]

    print(f'Part 1 answer is {sum(it.chain.from_iterable(part1(input_data).values()))}\n')
    print(f'Part 2 answer is {sum(it.chain.from_iterable(part2(input_data).values()))}')    