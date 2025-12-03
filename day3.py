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
Choose largest remaining number, and pick the first (leftmost occurrence).
Then repeat on the restricted sequence to the right of the latest choice.
When there are not enough digits left to complete k choices, backtrack.
'''
def max_joltage2(n, k=3):
    row = [int(x) for x in str(n)]
    if k == len(row):
        return n, list(range(len(row)))
    elif k > len(row):
        raise Exception("Not possible!")
    N = 9
    # ixes holds digit indices for the solution. We start off with a guard:
    ixes = [-1]
    while len(ixes) < k+1:
        try:
            # Look for N to the right of the solution so far (index 0 to begin
            # with):
            i = row.index(N, ixes[-1]+1)
        except ValueError: # Can't find N in the remaining digits
            # decrement N and start the search again
            if N > 1:
                N -= 1
            else: # i.e. N == 1
                # There are no zeros in the inputs, so we have reached the end 
                # of the search (unsuccesfully). Pop the last choice, and start 
                # searching for that number minus one.
                N = row[ixes.pop(-1)] - 1
            continue
        if len(ixes) == k:
            # Success! We have constructed the largest joltage, break and 
            # return
            ixes.append(i)
            break
        # Calculate how many digits we still need to find:
        num_left = k - len(ixes) + 1
        # And how many digits are to the right of the latest choice:
        num_digits_to_right = len(row)-1-i
        # If there are not enough digits left, decrement N and start the
        # search again.
        if num_left-1 > num_digits_to_right:
            N -= 1
        else:
            # OK, there are enough digits to the right to fulfil our search.
            # Add the latest digit to our solution, and start a new search
            # with N = 9 again
            ixes.append(i)
            N = 9
    # We were successful:
    ixes.pop(0) # Remove guard
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