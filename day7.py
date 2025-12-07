def string_replace(s, i, c = '|'):
    return s[:i] + c + s[(i+1):]
def splitter(data, VERBOSE=False):
    i = data[0].index('S')

    beams = set((i,))


    c = 0

    for r in range(1, len(data)):
        newbeams = set(())
        newrow = data[r]
        for i in beams:
            if newrow[i] == '^':
                newbeams.add(i-1)
                newbeams.add(i+1)
                c += 1
                # raise NotImplementedError
            else:
                newrow = string_replace(newrow, i)
                newbeams.add(i)
        if VERBOSE: print(f'{r:3d}', data[r], '  ', newrow)#string_replace(sample_input[r],i))
        beams = set(newbeams)
    return c

import itertools as it
import tqdm
def quantum(data, VERBOSE=False):
    i = data[0].index('S')
    from collections import defaultdict
    timelines = defaultdict(list)
    timelines[i] = ['']



    for r in tqdm.tqdm(range(1, len(data))):
        newtimelines = defaultdict(list)
        newrow = data[r]
        for i in timelines.keys():
            if newrow[i] == '^':
                newtimelines[i-1] += [x + 'L' for x in timelines[i]]
                newtimelines[i+1] += [x + 'R' for x in timelines[i]]
                # raise NotImplementedError
            else:
                newtimelines[i] += list(timelines[i])
        if VERBOSE: print(r, ':', newtimelines)
        timelines = dict(newtimelines)

    c = 0

    for x in it.chain.from_iterable(timelines.values()):
        c += 1

    return c




if __name__ == '__main__':
    # sample_input = open('day7_sample_input.txt').read().split('\n')[:-1]
    actual_input = open('c:/temp/day7_input.txt').read().split('\n')[:-1]
    print(f'Part 1 answer is {splitter(actual_input)}')
    print(f'Part 2 answer is {quantum(actual_input)}')