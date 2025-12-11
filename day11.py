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
            
    def traverse_part2(self, root, dest):
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
                # Probably better if we treat this as before, but...
                path_ix.pop(cur)
                path.pop(-1)
                last = path[-1]
                while path_ix[last]+1 == len(self.tree[last]):
                    path_ix.pop(last)
                    path.pop(-1)
                    try:
                        last = path[-1]
                    except IndexError:
                        return
                # pdb.set_trace()
                path_ix[last] += 1
                nxt = [self.tree[last][path_ix[last]],]

                pass














if __name__== '__main__':
    assert part1(sample_data) == 5

    print(f'Part 1 answer is', part1(actual_data))


