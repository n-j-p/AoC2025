import networkx
import pdb
import matplotlib.pyplot as plt
import tqdm
sample_data = open('day11_sample_input.txt', 'r').read().split('\n')[:-1]
sample_data2 = open('day11_sample_input_part2.txt', 'r').read().split('\n')[:-1]
actual_data = open('c:/temp/day11_input.txt', 'r').read().split('\n')[:-1]
def graphise(data):
    g = networkx.DiGraph()

    for row in data:
        rs = row.split(' ')

        node = rs[0][:-1]

        g.add_node(node)
        for n2 in rs[1:]:
            g.add_edge(node, n2)
    return g

def get_paths(data, a='you', b='out'):
    g = graphise(data)
    for path in networkx.all_simple_paths(g, a, b):
        yield path
def part1(data):
    c = 0
    for p in get_paths(data):
        c += 1
    return c
def part2(data):
    c = 0
    for p in tqdm.tqdm(get_paths(data, 'svr', 'out')):
        if 'dac' in p and 'fft' in p:
            c += 1
    return c
r'''
Let's do a DFS to begin with.



'''
class DiGraph():
    def __init__(self, connexions):
        self.connexions = connexions
        self.tree = {}
        for row in connexions:
            rs = row.split(' ')

            node = rs[0][:-1]

            self.tree[node] = []
            for n2 in rs[1:]:
                self.tree[node].append(n2)
    def traverse_part1(self, root, dest):
        assert root in self.tree
        cur = root
        
        path_ix = {}

        seen = set([])

        nxt = [cur,]
        path = []
        while len(nxt) > 0:
            cur = nxt.pop()
            if cur in seen:
                continue
            path.append(cur)
            if cur == dest:
                # pdb.set_trace()
                yield tuple(path)

                # Backtrack
                path.pop(-1)

                last = path[-1]
                while path_ix[last]+1 == len(self.tree[last]):
                    path_ix.pop(last)
                    path.pop(-1)
                    try:
                        last = path[-1]
                    except IndexError:
                        return

                path_ix[last] += 1
                # pdb.set_trace()
                cur = self.tree[last][path_ix[last]]
                path.append(cur)


            # if cur in path_ix:
                
            # seen.add(cur)
            # pdb.set_trace()
            if cur in path_ix:
                raise NotImplementedError('Cycle detected?')
            path_ix[cur] = 0
            try:
                
                nxt = [self.tree[cur][path_ix[cur]]]
            except KeyError: # Sink node
                continue
    r'''

    For part2 we need to enumerate paths rather than traverse each one.
    For example, in the sample data 'you' -> 'out', we get:

    [('you', 'bbb', 'ddd', 'ggg', 'out'),
     ('you', 'bbb', 'eee', 'out'),
     ('you', 'ccc', 'ddd', 'ggg', 'out'),
     ('you', 'ccc', 'eee', 'out'),
     ('you', 'ccc', 'fff', 'out')]

    Once we get to 'ggg' the second time there is no need to go to 'out' again.
    We could have recorded that there is just one path from 'ggg' to 'out', and
    add that to our enumeration.

    We would have:

    ('you', 'bbb', 'ddd', 'ggg', 'out') -> c[ggg] = 1; c[ddd] = 1; c[bbb] = c[ddd] = 1 (last two computed through backtracking)
    ('you', 'bbb', 'eee', 'out') -> c[eee] = 1; c[bbb] += c[eee] = 2
    ('you', 'ccc' ||| , 'ddd', 'ggg', 'out') -> c[ccc] = c[ddd] = 1
    ('you', 'ccc' ||| , 'eee', 'out') -> c[ccc] += c[eee] = 2
    ('you', 'ccc', 'fff', 'out')] -> c[fff] = 1; c[ccc] += c[fff] = 3

    and the you calculation is
    c['you'] = c['bbb'] + c['ccc'] = 5
    
    '''
    def enumerate_paths(self, root, dest):
        from collections import defaultdict

        # This holds the number of paths from current node to dest:
        npaths = defaultdict(int)
        npaths[dest] = 1

        cur = root      

        # Holds currently traversed path and child index:
        path = []

        while True:
            if cur in npaths:
                # Backtracking

                last2 = cur
                last,glast = path.pop(-1)

                # Backtrack until we get a node we haven't processed yet:
                while (last2 not in self.tree) or (glast+1 == len(self.tree[last])):
                    
                    # Update npaths
                    npaths[last] += npaths[last2]


                    last2 = last
                    try:
                        last,glast = path.pop(-1)
                    except IndexError: # Reached the end of the search
                        return npaths[root]
                npaths[last] += npaths[last2]
                path.append((last, glast+1))
                cur = self.tree[last][glast+1]
                continue
            path.append((cur, 0))

            try:
                cur = self.tree[cur][0]
            except KeyError: # sink node
                cur, _ = path.pop(-1)
                npaths[cur] = 0
            
  


                






def part2(data):
    dg = DiGraph(data)
    path1 = dg.enumerate_paths('svr','fft')*dg.enumerate_paths('fft','dac')*dg.enumerate_paths('dac','out')
    path2 = dg.enumerate_paths('svr','dac')*dg.enumerate_paths('dac','fft')*dg.enumerate_paths('fft','out') 

    return path1 + path2

if __name__== '__main__':
    assert part1(sample_data) == 5

    print(f'Part 1 answer is', part1(actual_data))

    assert part2(sample_data2) == 2

    print('Part 2 answer is', part2(actual_data))
