sample_data = '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,'+\
    '1698522-1698528,446443-446449,38593856-38593862,565653-565659,'+\
        '824824821-824824827,2121212118-2121212124'

import itertools as it

# Adapted from PE33.py
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
    ranges = data.split(',')
    LR =  [[int(x) for x in r.split('-')] for r in ranges]
    LRs = sorted(LR, key = lambda x: x[1])

    min_i = 0

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

if __name__ == '__main__':
    fpath = 'C:/temp/day2_input.txt'
    input_data = open(fpath).read().split('\n')[0]

    print(f'Part 1 answer is {sum(it.chain.from_iterable(part1(input_data).values()))}')