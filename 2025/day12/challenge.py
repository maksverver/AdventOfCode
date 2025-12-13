# Solution for additional challenge from reddit:
# https://old.reddit.com/r/adventofcode/comments/1pkm1ns/2025_day_12_part_3_perlfectly_wrapped_presents/

shapes = [(
    '###',
    '##.',
    '##.',
), (
    '###',
    '##.',
    '.##',
), (
    '.##',
    '###',
    '##.',
), (
    '##.',
    '###',
    '##.',
), (
    '###',
    '#..',
    '###',
), (
    '###',
    '.#.',
    '###',
)]

def Rotate(grid):
    H = len(grid)
    W = len(grid[0])
    return tuple(''.join(grid[W - 1 - r][c] for r in range(W)) for c in range(H))

def Flip(grid):
    return tuple(''.join(row) for row in zip(*grid))


W = 8
H = 6

# For each shape, a list of integers representing the bitmasks corresponding
# with possible placements of this shape.
options = []

# Generate possible placements of shapes after rotating and flipping.
# Code below assumes each shape is 3x3 in size.
variations = []
for shape in shapes:
    vars = set()
    for _ in range(4):
        vars.add(shape)
        vars.add(Flip(shape))
        shape = Rotate(shape)
    options.append([
        sum(2**((i + r)*W + (j + c))
                for i, row in enumerate(var)
                for j, ch in enumerate(row)
                if ch == '#')
        for r in range(H - 3 + 1)
        for c in range(W - 3 + 1)
        for var in vars
    ])


def CountSolutions(pos, grid):
    if pos == len(options):
        return 1

    return sum(
        CountSolutions(pos + 1, grid | mask)
        for mask in options[pos]
        if (grid & mask) == 0)


def PrintSolutions():
    choices = []

    def Print():
        grid = [['.']*W for _ in range(H)]
        for i, mask in enumerate(choices):
            for r in range(H):
                for c in range(W):
                    if (mask & (1 << (W*r + c))) != 0:
                        assert grid[r][c] == '.'
                        grid[r][c] = chr(ord('a') + i)
        for row in grid:
            print(''.join(row))
        print()

    def Search(pos, grid):
        if pos == len(options):
            return Print()

        for mask in options[pos]:
            if (grid & mask) == 0:
                choices.append(mask)
                Search(pos + 1, grid | mask)
                choices.pop()

    Search(0, 0)

if __name__ == '__main__':

    print(CountSolutions(0, 0))  # 11464
    #PrintSolutions()
