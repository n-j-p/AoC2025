sample_data = ['L68',
    'L30',
    'R48',
    'L5',
    'R60',
    'L55',
    'L1',
    'L99',
    'R14',
    'L82']

def rotate(input,part=1,VERBOSE=False):
    parsed = [(-1 if z[0] == 'L' else 1)*int(z[1:]) for z in input]
    if VERBOSE: print(parsed)

    t = 50
    if VERBOSE: print(t, end = ' ')
    c = 0
    for x in parsed:
        t = (t + x) % 100
        if VERBOSE: print(t, end=' ')
        if t == 0:
            c += 1
    return c

def rotate2(input):
    parsed = [(-1 if z[0] == 'L' else 1)*int(z[1:]) for z in input]
    print(parsed)

    c = 0
    x = 50
    for t in parsed:

        passed = False
        on = False
        print(f'{x}, {t} -> {x+t}', end = ' ')
        
        if x+t > 100:
            n_times_passed = (x+t) // 100
        elif x + t < 0 and x > 0:
            n_times_passed = 1 + (-(x+t)) // 100
        else:
            n_times_passed = 0
        x = (x+t) % 100
        print(f'= {x}', end = ' ')
        on = x == 0
        print(on, n_times_passed)
        if n_times_passed > 0 and on:
            c += n_times_passed
            pass
        else:
            c += on + n_times_passed
    return c
def rotate3(input, VERBOSE=False):
    parsed = [(-1 if z[0] == 'L' else 1)*int(z[1:]) for z in input]
    if VERBOSE: print(parsed)

    c = 0
    x = 50
    for t in parsed:
        if VERBOSE: print(x, t, (t+x) % 100, end=': ')
        assert t != 0
        if x == 0:
            if t < 0:
                ci = (-t) // 100
            else:
                ci = t // 100
        else:
            if t < 0:
                if t + x > 0:
                    ci = 0
                else:
                    ci = 1 + (-(t+x)) // 100
            else:
                if t + x < 100:
                    ci = 0
                else:
                    ci = (t+x) // 100
        if VERBOSE: print(ci)
        x = (x + t) % 100
        c += ci
    return c

if __name__ == '__main__':
    print()

    # Read in actual data
    fpath = '../day1_input.txt'
    data = open(fpath).read().split('\n')[:-1]
    
    print(f'Part 1 answer is {rotate(data)}')
    print(f'Part 2 answer is {rotate3(data)}')

