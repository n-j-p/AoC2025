def string_replace(s, i, c = '|'):
    return s[:i] + c + s[(i+1):]
def splitter(data):
    i = data[0].index('S')

    beams = set((i,))


    c = 0

    for r in range(1, len(data)):
        newbeams = set(())
        newrow = data[r]
        for i in beams:
            if newrow[i] == '^':
                newbeams.add(i-1)
                newbeams.add(i+1)
                c += 1
                # raise NotImplementedError
            else:
                newrow = string_replace(newrow, i)
                newbeams.add(i)
        print(f'{r:3d}', data[r], '  ', newrow)#string_replace(sample_input[r],i))
        beams = set(newbeams)
    return c

if __name__ == '__main__':
    sample_input = open('day7_sample_input.txt').read().split('\n')[:-1]

    print(splitter(sample_input))