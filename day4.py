import itertools as it

sample_data = ['..@@.@@@@.',
    '@@@.@.@.@@',
    '@@@@@.@.@@',
    '@.@@@@..@.',
    '@@.@@@@.@@',
    '.@@@@@@@.@',
    '.@.@.@.@@@',
    '@.@@@.@@@@',
    '.@@@@@@@@.',
    '@.@.@@@.@.']

class Grid():
    def __init__(self, plan):
        self.plan = plan
        self.Rx = len(plan)
        self.Cx = len(plan[0])

    def get_block(self, r, c):
        rows = self.plan[max(0,r-1):(r+2)]
        return [r[max(0,c-1):(c+2)] for r in rows]
    
    def paper_index_generator(self):
        for r in range(self.Rx):
            for c in range(self.Cx):
                if self.plan[r][c] == '@':
                    yield (r,c)
    
    def count_free(self, return_ixes=False):
        ct = 0
        ixes = []
        for r,c in self.paper_index_generator():
            block = self.get_block(r,c)
            n = 0
            for x in it.chain.from_iterable(block):
                if x == '@':
                    n += 1
                if n == 5:
                    break
            if n <= 4:
                ct += 1
                ixes.append((r,c))
        if return_ixes:
            return ct, ixes
        else:
            return ct
    def update(self, ixes):
        new_plan = [x for x in self.plan] # make a copy!
        for r,c in ixes:
            new_plan[r] = new_plan[r][:c] + '.' + new_plan[r][(c+1):]
        self.plan = new_plan
    def remove_all(self):
        ct = 1
        tot = 0
        while ct > 0:
            ct, ix = self.count_free(True)
            tot += ct
            #print(ct)
            self.update(ix)
        return tot

    
if __name__ == '__main__':
    actual_data = open('c:/temp/day4_input.txt').read().split('\n')[:-1]
    print(f'Part 1 answer is {Grid(actual_data).count_free()}')

    print(f'Part 2 answer is {Grid(actual_data).remove_all()}')
