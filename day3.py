sample_input= ['987654321111111',
    '811111111111119',
    '234234234234278',
    '818181911112111']

import itertools as it
def max_joltage(data):
    # Brute-force, just look through 2-combinations of the input data
    mxs = []
    for row in data:
        mx = 0
        for x in it.combinations(row, 2):
            mx = max(mx, int(''.join(x)))
        # print(mx)
        mxs.append(mx)
    return mxs

r'''
Part 2 algorithm outline:
If there is a 9, choose that. In fact, choose the left-most 9 since that will
always give a larger joltage than anything to the right. Then we search for
the next 9 (to the right of our first digit). Failing that search for 8, 7, ...
If there were infinite digits that would be the complete algorithm. However, if
there are not enough digits remaining to the right of our latest choices, we 
need to backtrack.
'''
def max_joltage2(n, k=3):
    row = [int(x) for x in str(n)]
    if k == len(row):
        return n, list(range(len(row)))
    elif k > len(row):
        raise Exception("Not possible!")
    # ixes holds digit indices for the solution. We start off with a guard:
    ixes = [-1]

    N = 9
    while len(ixes) < k+1:
        try:
            # Look for N to the right of the solution so far (index 0 to begin
            # with):
            i = row.index(N, ixes[-1]+1)
        except ValueError: # Can't find N in the remaining digits
            # If we can,
            if N > 1:
                # decrement N and start the search again
                N -= 1
            else: # here N == 1 so we can't decrement as 
                # there are no zeros in the inputs. We have reached the end 
                # of the search (unsuccessfully). Pop the last choice, and 
                # start searching for that number minus one.
                N = row[ixes.pop(-1)] - 1
            continue
        if len(ixes) == k:
            # Success! We have constructed the largest joltage, break and 
            # return
            ixes.append(i)
            break

        # o.w.:
        # Calculate how many digits we still need to find:
        num_digits_remaining = k - len(ixes) + 1
        # And how many digits are to the right of the latest choice:
        num_digits_to_right = len(row)-1-i
        # If there are not enough digits left, decrement N and start the
        # search again.
        if num_digits_remaining-1 > num_digits_to_right:
            N -= 1
        else:
            # OK, there are enough digits to the right to (potentially) fulfil 
            # our search.
            # Add the latest digit to our solution, and start a new search
            # with N = 9 again
            ixes.append(i)
            N = 9

    # Yes! We were successful:
    ixes.pop(0) # Remove guard
    # Return solution
    return int(''.join([str(row[i]) for i in ixes])), ixes

def part1():
    actual_input = open('c:/temp/day3_input.txt').read().split('\n')[:-1]
    print(f'Part 1 solution is {sum(max_joltage(actual_input))}')
def part2():
    c = 0
    actual_input = open('c:/temp/day3_input.txt').read().split('\n')[:-1]
    for r in actual_input:
        c += max_joltage2(int(r), 12)[0]
    print(f'Part 2 solution is {c}')


if __name__ == '__main__':
    part1()
    part2()