class Range():
    def __init__(self, lo, hi):
        self.lo = lo
        self.hi = hi
    def contains(self, x):
        return x >= self.lo and x <= self.hi
    
sample_data = ['3-5',
    '10-14',
    '16-20',
    '12-18',
    '',
    '1',
    '5',
    '8',
    '11',
    '17',
    '32']

def parse(data):
    ranges = []
    for i, line in enumerate(data):
        if len(line) > 0:
            LH = line.split('-')
            # print([int(x) for x in LH])
            ranges.append(Range(*[int(x) for x in LH]))
        else:
            break
    ingredients = []
    for i in data[(i+1):]:
        ingredients.append(int(i))

    return ranges, ingredients
            
def part1(data):
    ranges, ingredients = parse(data)

    c = 0

    for i in ingredients:
        spoiled = True
        for rng in ranges:
            if rng.contains(i):
                spoiled = False
                break
        if spoiled:
            pass
            # print(f'{i} spoiled')
        else:
            # print(f'{i} not spoiled')  
            c += 1
    return c

class NoIntersection(Exception):
    pass

class Range2(Range):
    def __repr__(self):
        return f'{self.lo}-{self.hi}'
    def intersects(self, other):
        return self.contains(other.lo) or self.contains(other.hi)
        # return self.hi >= other.lo or self.lo <= other.hi
    def union(self, other):
        if self.contains(other.lo) and not self.contains(other.hi):
            # self:  [  ]
            # other:   [  ]
            return Range2(self.lo, other.hi)
        elif self.contains(other.hi) and not self.contains(other.lo):
            # self:      [  ]
            # other:   [  ]
            return Range2(other.lo, self.hi)
        elif self.contains(other.hi) and self.contains(other.lo):
            # self:   [     ]
            # other:  [  ]
            return Range2(self.lo, self.hi)
        elif other.contains(self.hi) and other.contains(self.lo):
            # self:     []
            # other: [    ]
            return Range2(other.lo, other.hi)
        else:
            raise NoIntersection

def part2(data):
    ranges, _ = parse(data)
    ranges = [Range2(r.lo, r.hi) for r in ranges]

    # print(ranges)
    finished = []
    while len(ranges) > 1:
        R = ranges.pop(0)
        # print('processing',R)
        R_separate = True
        for i,S in enumerate(ranges):
            try:
                R2 = R.union(S)
            except NoIntersection:
                continue
            # print(R, 'intersects',S, 'union =',R2)
            ranges.pop(i)

            R_separate = False
            break
        if R_separate:
            # print('no intersections, moving to finished')
            finished.append(R)
        else:
            # print('appending',R2,'to ranges')
            ranges.append(R2)

        # print(ranges, finished)
        # print()

    finished_ranges = finished + ranges
    c = 0
    for rng in finished_ranges:
        c += rng.hi - rng.lo + 1
    return c




if __name__ == '__main__':
    actual_input = open('c:/temp/day5_input.txt').read().split('\n')[:-1]

    # Part 1
    print(f'Part 1 answer is {part1(actual_input)}')

    # Part 2
    print(f'Part 2 answer is {part2(actual_input)}')