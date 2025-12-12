import pdb
import numpy as np
import itertools as it

actual_input = open('c:/temp/day12_input.txt').read().split('\n')[:-1]

class Region():
    def __init__(self, line):
        self.width = int(line.split('x')[0])
        self.height = int(line.split('x')[1].split(':')[0])
        self.npres = [int(x) for x in line.split(':')[1].split(' ')[1:]]
        pass
    def __repr__(self):
        return f'({self.width}, {self.height}): {self.npres}'
def parse(data):
    print(data)
    shapes = []
    regions = []
    for line in data:
        if 'x' in line:
            regions.append(Region(line))
        else:
            shapes.append(line)
    s2 = it.pairwise([-1,] + [i for i,x in enumerate(shapes) if len(x) == 0])
    shapes2 = {}
    for x in s2:
        shapes2[int(shapes[x[0]+1][:-1])] = shapes[x[0]+2:x[1]]
    # pdb.set_trace()
    return regions, shapes2
