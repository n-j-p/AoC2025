sample_input= ['987654321111111',
    '811111111111119',
    '234234234234278',
    '818181911112111']

def test_part2():
    from day3 import max_joltage2
    ans = [987654321111,
           811111111119,
           434234234278,
           888911112111]

    for i,ns in enumerate(sample_input):
        n = int(ns)
        assert max_joltage2(n, 12)[0] == ans[i]
        