import itertools as it
def D2(p,q):

    return (p[0]-q[0])**2 + (p[1]-q[1])**2 + (p[2]-q[2])**2
import tqdm


class UnionFind():
    '''Union-find algorithm, see Sedgewick (1990) Algos in C, chapter 30.'''
    def __init__(self, n):
        self.n = n
        self.dad = [0 for _ in range(n)]
        self.tree_sizes = [1 for _ in range(n)]

    def find(self, x, y):
        return self.get_root(x), self.get_root(y)

    def union(self, x,y):
        xr,yr=self.find(x,y)
        if xr != yr: 
            
            # Choose the right node as root, 
            # this is important for performance!
            if self.tree_sizes[xr] < self.tree_sizes[yr]:
                self.dad[xr] = yr
                self.tree_sizes[yr] += self.tree_sizes[xr]
            else:
                self.dad[yr] = xr
                self.tree_sizes[xr] += self.tree_sizes[yr]                
            
    def get_root(self, x):
        while self.dad[x] > 0:
            x = self.dad[x]
        return x

    def get_size(self, x):
        return self.tree_sizes[self.get_root(x)]



def connect(data, max_connections):
    T = [[int(x) for x in y.split(',')] for y in data]

    # print(T)

    all_distances = []
    i = 1
    for j,k in tqdm.tqdm(it.combinations(range(len(T)),2), total=len(T)*(len(T)-1)//2):
        x = T[j]
        y = T[k]
        # print(i,x,y)
        all_distances.append((D2(x,y), j, k, x, y))
        i += 1
    all_distances=sorted(all_distances)
    # print(all_distances[:20])
    uf = UnionFind(len(T)+1)
    n_connections = 0
    i = 0
    while n_connections < max_connections:
        j,k = all_distances[i][1]+1, all_distances[i][2]+1
        x,y = all_distances[i][3], all_distances[i][4]
        # print(x,y, end=' ')
        i += 1
        # print(uf.get_root(j), uf.get_root(k))
        n_connections += 1 
        if uf.get_root(j) == uf.get_root(k):
            # print('already connected')
            continue
        # print("joining")
        uf.union(j,k)
    return uf

def part1(data, max_connections=10):
    z=connect(data, max_connections)

    from collections import Counter
    c = Counter()

    c.update([z.get_root(x) for x in range(len(data)+1)][1:])
    from functools import reduce
    return reduce(lambda x,y: x*y, sorted(c.values())[-3:])

def finished(uf_struct):
    seen_zero = False
    for x in uf_struct.dad[1:]:
        if x == 0:
            if seen_zero:
                return False
            seen_zero = True
    return True
def part2(data):
    T = [[int(x) for x in y.split(',')] for y in data]

    # print(T)

    all_distances = []
    i = 1
    for j,k in tqdm.tqdm(it.combinations(range(len(T)),2), total=len(T)*(len(T)-1)//2):
        x = T[j]
        y = T[k]
        # print(i,x,y)
        all_distances.append((D2(x,y), j, k, x, y))
        i += 1
    all_distances=sorted(all_distances)
    # return all_distances

    uf = UnionFind(len(T)+1)
    for i in tqdm.tqdm(range(len(all_distances))):
        j,k = all_distances[i][1]+1, all_distances[i][2]+1
        x,y = all_distances[i][3], all_distances[i][4]
        if finished(uf):
            break
        uf.union(j,k)
        # print(uf.dad)
        last = (x,y)
    return last[0][0]*last[1][0]
if __name__ == '__main__':
    actual_input = open('c:/temp/day8_input.txt', 'r').read().split('\n')[:-1]
    sample_input = open('./day8_sample_input.txt', 'r').read().split('\n')[:-1]

    print(f'Part 1 answer is {part1(actual_input, 1000)}')
    print(f'Part 2 answer is {part2(actual_input)}')
