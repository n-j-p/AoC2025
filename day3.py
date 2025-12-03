sample_input= ['987654321111111',
    '811111111111119',
    '234234234234278',
    '818181911112111']

import itertools as it
def max_joltage(data):
    mxs = []
    for row in data:
        mx = 0
        for x in it.combinations(row):
            # print(int(''.join(x)))
            mx = max(mx, int(''.join(x)))
            # print(' ',mx)
        print(mx)
        mxs.append(mx)
    return mxs

def max_joltage2(n, k=3):
    row = [int(x) for x in str(n)]
    if k == len(row):
        return n, list(range(len(row)))
    elif k > len(row):
        raise Exception("Not possible!")
    N = 9
    ixes = [-1]
    while len(ixes) < k+1:
        try:
            i = row.index(N, ixes[-1]+1)
        except ValueError:
            if N == 1:
                N = row[ixes.pop(-1)] - 1
            else:
                N -= 1
                if N <= 0:
                    import pdb
                    pdb.set_trace()
            continue
        num_left = k - len(ixes) + 1
        num_digits_to_right = len(row)-1-i
        if len(ixes) == k:
            ixes.append(i)
            break
        if num_left > num_digits_to_right:
        # if i + k > len(ixes):
        # if i == len(ixes)-1 and len(ixes) < k+1:
            # import pdb
            # pdb.set_trace()
            N -= 1
            # pass
        else:

            ixes.append(i)
            N = 9
    ixes.pop(0) # Remove guard
    return int(''.join([str(row[i]) for i in ixes])), ixes