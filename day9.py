def D1(x,y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1])
def A(x,y):
    return abs((x[0]-y[0]+1)*(x[1]-y[1]+1))
import itertools as it
import tqdm
def part1(data):
    pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in data]]
    # pts = [[int(x) for x in y] for y.split(",") in sample_input]
    largest_D = 0
    loc = None
    for x,y in tqdm.tqdm(it.combinations(pts, 2), total = len(pts)*(len(pts)-1)//2):
        # print(x,y, D1(x,y))
        D = A(x,y)
        if D > largest_D:
            loc = (x,y)
            largest_D = D
    print(loc)
    return largest_D
def classify_pts(data):
    corners = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in data]]
    pts = {pt: 'c' for pt in corners}
    for x,y in it.pairwise(corners):
        print(x,y)
        if x[0] == y[0]: # vertical
            mn = min(x[1], y[1])
            mx = max(x[1], y[1])
            for z in range(mn+1, mx):
                pts[x[0], z] = 'v'
        elif x[1] == y[1]: # horizontal
            mn = min(x[0], y[0])
            mx = max(x[0], y[0])
            for z in range(mn+1, mx):
                pts[z, x[1]] = 'h'
        else:
            raise ValueError
    return pts
class OutsideRectangle(Exception):
    pass


def line_generator(pt1, pt2):
    '''

      -----pt2
      |    |
    pt1-----

    '''
    mn_x = min(pt1[0], pt2[0])
    mx_x = max(pt1[0], pt2[0])
    for z in range(mn_x+1, mx_x):
        yield (z, pt1[1],'h')
    mn_y = min(pt1[1], pt2[1])
    mx_y = max(pt1[1], pt2[1])
    for z in range(mn_y+1, mx_y):
        yield (pt1[0], z,'v')
    for z in range(mn_x+1, mx_x):
        yield (z, pt2[1],'h')
    for z in range(mn_y+1, mx_y):
        yield (pt2[0], z,'v')
    

def Rok(x,y, pt_class_dict):
    touched_corner = False
    for x,y,t in line_generator(x,y):
        try:
            pt_type = pt_class_dict[(x,y)]
        except KeyError:
            if touched_corner:
                return False
            continue
        if pt_type == 'c':
            touched_corner = True
        if (t == 'h' and pt_type == 'v') or (t == 'v' and pt_type == 'h'):
            return False
    return True

def part2(data):
    pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in data]]
    z = classify_pts(data)
    # pts = [[int(x) for x in y] for y.split(",") in sample_input]
    allcombos = []
    for x,y in tqdm.tqdm(it.combinations(pts, 2), total = len(pts)*(len(pts)-1)//2):
        allcombos.append((A(x,y), x, y))
    srt_allcombos = sorted(allcombos)[::-1]

    mxA = 0
    loc = None
    for D,pt1, pt2 in tqdm.tqdm(srt_allcombos):
        if Rok(pt1, pt2, z):
            return D, pt1, pt2
    

if __name__ == '__main__':
    sample_input = open('./day9_sample_input.txt', 'r').read().split('\n')[:-1]
    sample_pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in sample_input]]
    print(sample_input)
    print(part1(sample_input))

    actual_input = open('./day9_input.txt', 'r').read().split('\n')[:-1]
    pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in actual_input]]
    print(actual_input)
    print(part1(actual_input))
