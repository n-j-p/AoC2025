sample_input= ['987654321111111',
    '811111111111119',
    '234234234234278',
    '818181911112111']

import itertools as it
def max_joltage(data, k=2):
    mxs = []
    for row in data:
        mx = 0
        for x in it.combinations(row, k):
            # print(int(''.join(x)))
            mx = max(mx, int(''.join(x)))
            # print(' ',mx)
        print(mx)
        mxs.append(mx)
    return mxs