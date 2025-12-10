import pdb
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
    for x,y in it.pairwise(corners + [corners[0],]):
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

    actual_input = open('c:/temp/day9_input.txt', 'r').read().split('\n')[:-1]
    pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in actual_input]]
    print(actual_input)
    print(part1(actual_input))


r'''

Analysis.

We have a series of points which are rectilinearlly connected, i.e. subsequent
points share either the same x- or the same y-coordinate (with the other 
different). Each point is set as a corner, and lines connecting each corner
are either vertical or horizontal lines. All of these points are red or green 
squares as per the problem description.

Joining all the points gives us a closed curve and thus an interior and 
exterior. All interior points are coloured green. Given two corners defining
a rectangle we will have corresponding lines between four vertices of the 
rectangle

Now we can trace each line and the rectangle is OK (entirely on red or 
green squares) so long as no part of the line lies in the exterior of the
defined close curve.

Wlog let's consider a horizontal line (can flip to vertical just by changing
a few things).

We hit an exterior point if: 

1. the line passes an odd number (including one) of consecutive vertical points
and then hits an empty square, e.g.:

---.
 I | E
 >>>>>
   |
(I and E designate interior and exterior parts of the curve.)

If we pass through two vertical lines, e.g.

---. E
   |.----
 I ||
 >>>>>>
   || I
   ..

we are still in the interior. Passing through three verticals lands us in
the exterior.

However, if we don't break through to an empty square (i.e. the line we are 
tracing ends on a vertical or corner square), we are still OK.

2. we are leave a corner square and we hit an empty square that is in the 
exterior, the rectangle is not OK. For this we classify corners as either
external or internal corners:

External:  Internal:

---.        ---.   
   | E         | I 
 I |         E |   
       
A corner is external if the two empty squares on either side are outside
the curve and internal if the two empties are inside squares.

If we have a corner designated as one type, the next corner is then the 
other type if the second corner is oriented like:

------.
      |  E/I
 I/E  |
      .-----

and the same type if:
      

------.
      |
 I/E  | I/E
    --.

Thus starting with one corner and designating it either internal or external
(not sure how to start this), we can go around the curve and designate
each corner as either internal or external.

If the line we are tracing leaves a corner and touches an empty space we
can tell straight away if we are in the exterior or not.

One complication is if we start the line tracing on a vertical wall:
 -|||-
  |X>>>
  |||
Is the empty square we first reach interior or exterior?


'''

# Let's start by designating corner types:

def classify2(data,start_type='e'):
    pts = [(int(x[0]), int(x[1])) for x in [y.split(",") for y in data]]
    z = classify_pts(data)
    corner_types = {}
    corner_types[pts[0]] = start_type # assume to begin with
    for c1, c2 in it.pairwise(pts + [pts[0],]):
        print(c1,c2)
        if c1[0] == c2[0]: # line connecting these corners is vertical
            if (c1[0]-1, c1[1]) in z:
                #
                # --X c1
                #   |
                #   X c2
                #
                # or:
                #
                #   X c2
                #   |
                # --X c1
                #
                if (c2[0]-1, c2[1]) in z:
                    corner_types[c2] = corner_types[c1]
                else:
                    corner_types[c2] = 'i' if corner_types[c1] == 'e' else 'e'
            elif (c1[0]+1, c1[1]) in z:
                if (c2[0]+1, c2[1]) in z:
                    corner_types[c2] = corner_types[c1]
                else:
                    corner_types[c2] = 'i' if corner_types[c1] == 'e' else 'e'
            else:
                raise NotImplementedError('Unknown')
        else: # line connecting the two corners is horizontal
            if (c1[0], c1[1]-1) in z:
                if (c2[0], c2[1]-1) in z:
                    corner_types[c2] = corner_types[c1]
                else:
                    corner_types[c2] = 'i' if corner_types[c1] == 'e' else 'e'
            elif (c1[0], c1[1]+1) in z:
                if (c2[0], c2[1]+1) in z:
                    corner_types[c2] = corner_types[c1]
                else:
                    corner_types[c2] = 'i' if corner_types[c1] == 'e' else 'e'
            else:
                raise NotImplementedError('unknown')
    return z, pts, corner_types

# The above seems to be correct, at least on the sample_input

r'''

The concern above is equally valid if we start in an empty square. Is it
interior or exterior? However, in both cases we can trace the line in the
other direction (i.e. always starting from a corner). Leaving the corner we 
either are on a horizontal or another corner, which is OK, or an empty 
square in which case we can check. What about:

  E |
---X>>?
   ||
   ..

In this case, leaving the corner, we know that if the wall wasn't there it
would be exterior, so crossing it puts us in the interior. Or, consider 
that we start on a vertical wall, which counts for the odd/even calculation as
above. So, when we start tracing the line, start with vertical_wall_count
equal to one. (Counter reset once we leave a series of consecutive walls).

'''

def trace_from_corner(p, q):
    '''
.---q
|   |
p---.

Here we generate the two lines radiating from p
    '''

    px, py = p
    qx, qy = q

    # First do horizontal line:
    if qx > px:
        for x in range(px+1, qx+1):
            yield ('h', x, py)
    else:
        for x in range(px-1,qx-1,-1):
            yield ('h', x, py)

    # Next vertical line:
    if qy > py:
        for y in range(py+1, qy+1):
            yield ('v', px, y)
    else:
        for y in range(py-1, qy-1, -1):
            yield ('v', px, y)

class Curve():
    def __init__(self, data, start_type='e'):
        z, _, corner_types = classify2(data, start_type=start_type)
        self.corner_types = corner_types
        self.curve_pts = z
        
    def Rok(self, p, q):
        trace_gen = trace_from_corner(p, q)
        # Start with the horizontal trace:
        # We always start on a corner:
        cur_loc = p
        cur_type = 'c'
        perpendicular_wall_count = 1 # see above, just incase the next square
                                     # is a perp. wall
        for trace_direction, x, y in trace_gen:


            if trace_direction == 'v':
                break

            nxt_loc = (x,y)
            try:
                nxt_type = self.curve_pts[nxt_loc]
            except KeyError: # empty square:
                nxt_type = '.'
            # Horizontal trace:
            #       next
            # last \ c  v   h   .
            # -------------------
            #   c  | OK X1  OK  X4
            #   v  | OK X2  N/A X5
            #   h  | OK N/A OK  N/A
            #   .  | OK X2  N/A OK
            # OK entries: do nothing
            # N/A entries: shouldn't happen (check!)
            # X1 c -> v, ok for now, but wall_count = 2 (??)
            # X2 v,. -> v, increment wall count
            # X4 c -> ., check if corner is internal/external, possibly reject
            # X5 v -> ., check wall_count, possibly reject 
            #    . -> ., should be OK as we should always be internal if we just left .
            if nxt_type == 'c':
                # It is always OK to be on a corner, reset wall count:
                perpendicular_wall_count = 0
            elif nxt_type == 'h':
                if cur_type == 'v' or cur_type == '.':
                    raise NotImplementedError("Shouldn't happen...")
                # Otherwise, OK to slide along horizontal wall
                perpendicular_wall_count = 0
            elif nxt_type == '.':
                if cur_type == 'h':
                    raise NotImplementedError("Shouldn't happen...")
                elif cur_type == '.':
                    pass
                    # moving from . to . should always be OK because we should
                    # be in an interior square if we haven't quit yet...
                elif cur_type == 'c':
                    if self.corner_types[cur_loc] == 'e':
                        # We moved from a corner to an exterior point
                        return False
                    else:
                        # now we are in an interior point
                        perpendicular_wall_count = 0
                elif cur_type == 'v':
                    if perpendicular_wall_count % 2 == 1:
                        # import pdb
                        # pdb.set_trace()
                        # After a sequence of vertical walls we are outside
                        return False
                    else:
                        # o.w. we are on the inside 
                        perpendicular_wall_count = 0
            elif nxt_type == 'v':
                if cur_type in ['c','.']:
                    perpendicular_wall_count = 1
                elif cur_type == 'v':
                    perpendicular_wall_count += 1
                elif cur_type == 'h':
                    raise NotImplementedError("Shouldn't happen")
                else:
                    raise Exception("Unknown")
            cur_loc = nxt_loc
            cur_type = nxt_type
                
        # print('now process vertical trace')
        # If there is no vertical, we are done:
        if trace_direction == 'h':
            return True
        
        # Reset back to p:
        cur_loc = p
        cur_type = 'c'
        nxt_loc = (x,y)
        while True:
            try:
                nxt_type = self.curve_pts[nxt_loc]
            except KeyError: # empty square:
                nxt_type = '.'
            # Vertical trace:
            # is similar to horizontal trace but we swap v and h:
            #       next
            # last \ c  v   h   .
            # -------------------
            #   c  | OK OK  X1  X4
            #   v  | OK OK  N/A N/A
            #   h  | OK N/A X2  X5
            #   .  | OK N/A X2  OK
            # OK entries: do nothing
            # N/A entries: shouldn't happen (check!)
            # X1 c -> h, ok for now, but wall_count = 2 (??)
            # X2 h,. -> h, increment wall count
            # X4 c -> ., check if corner is internal/external, possibly reject
            # X5 h -> ., check wall_count, possibly reject 
            #    . -> ., should be OK as we should always be internal if we just left .
            if nxt_type == 'c':
                # It is always OK to be on a corner, reset wall count:
                perpendicular_wall_count = 0
            elif nxt_type == 'v':
                if cur_type == 'h' or cur_type == '.':
                    raise NotImplementedError("Shouldn't happen...")
                # Otherwise, OK to slide along vertical wall
                perpendicular_wall_count = 0
            elif nxt_type == '.':
                if cur_type == 'v':
                    raise NotImplementedError("Shouldn't happen...")
                elif cur_type == '.':
                    pass
                    # moving from . to . should always be OK because we should
                    # be in an interior square if we haven't quit yet...
                elif cur_type == 'c':
                    if self.corner_types[cur_loc] == 'e':
                        # We moved from a corner to an exterior point
                        return False
                    else:
                        # now we are in an interior point
                        perpendicular_wall_count = 0
                elif cur_type == 'h':
                    # import pdb
                    # pdb.set_trace()
                    if perpendicular_wall_count % 2 == 1:
                        # import pdb
                        # pdb.set_trace()
                        # After a sequence of horizontal walls we are outside
                        return False
                    else:
                        # o.w. we are on the inside 
                        perpendicular_wall_count = 0
            elif nxt_type == 'h':
                if cur_type in ['c','.']:
                    perpendicular_wall_count = 1
                elif cur_type == 'h':
                    perpendicular_wall_count += 1
                elif cur_type == 'v':
                    raise NotImplementedError("Shouldn't happen")
                else:
                    raise Exception("Unknown")
            try:
                _,x,y = next(trace_gen)
            except StopIteration:
                # Done! Success!
                return True
            cur_loc = nxt_loc
            cur_type = nxt_type
            nxt_loc = (x,y)

            # if y in [48719, 50049]:
            #     import pdb
            #     pdb.set_trace()
            #     pass



def part2_new(data):
    c = Curve(data)
    corners = list(c.corner_types.keys())
    # corners += [corners[0],]

    print()
    for p,q in it.combinations(corners,2):
        ok = c.Rok(p,q) and c.Rok(q,p)
        if ok:
            print(p,q, ok, A(p,q))
        else:
            print(p,q,ok)

def part2_actual(data, min_size=2e9):
    c = Curve(data, start_type='i')
    pts = list(c.corner_types.keys())

    allcombos = []
    for x,y in tqdm.tqdm(it.combinations(pts, 2), total = len(pts)*(len(pts)-1)//2):
        allcombos.append((A(x,y), x, y))
    srt_allcombos = sorted(allcombos)[::-1]
    for A_, p, q in tqdm.tqdm(srt_allcombos):
        if A_ > min_size:
            continue
        # px,py = p
        # qx,qy = q
        # if (px > 1723 and px <= 94523)
        if c.Rok(p,q) and c.Rok(q,p):
            print(p,q)
            return A_
    # return srt_allcombos